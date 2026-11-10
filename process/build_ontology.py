"""Build an OWL ontology from an rs.tdwg.org term list and its axioms file.

An ontology is described in rs.tdwg.org in three parts (see process-ontology.md,
and the TDWG Standards Documentation Specification, Section 4.4.2.2):

- the basic term list: the current-terms CSV of a dataset (e.g. bdqffdq/bdqffdq.csv)
  and its column mappings, processed by process.py like any other term list;
- the axioms file (<dataset>/<dataset>-axioms.ttl), a vocabulary extension term list
  holding the axioms that cannot be rows because they need blank nodes (class
  expressions such as owl:Restriction, owl:AllDisjointClasses, owl:AllDifferent);
- the vocabulary record (vocabularies/, vocabularies-versions/): its IRI is the
  ontology IRI, and its label, description, license, and current version give the
  ontology header.

This script combines them into one ontology document and writes it as Turtle,
RDF/XML, and JSON-LD. The term statements are made from the CSV with the same
rules as the rs.tdwg.org serializer (html/restxq.xqm, page:property-value-pairs),
so the ontology and the per-term responses state the same things.

To keep the result OWL 2 DL, the script:
- declares every annotation property it uses, and every datatype that is not in
  the OWL 2 datatype map (e.g. xsd:date);
- replaces annotations with reserved properties that OWL 2 DL does not allow, by
  default rdf:value -> skos:notation (SDS 4.5.4 uses rdf:value for controlled value
  strings). A substitution that would duplicate an existing statement is dropped.
  The ontology header records the substitutions in an rdfs:comment.

Checks (the script exits with an error if one fails):
- every IRI in the term namespace used in the axioms file is a term in the CSV;
- every term has an rdf:type;
- with ROBOT (http://robot.obolibrary.org/, optional): the ontology is in the
  OWL 2 DL profile, and consistent (HermiT). ROBOT, through the OWL API, then also
  writes the Turtle and RDF/XML files. Without ROBOT, rdflib writes all three files
  and the script reports that the ontology was not validated.

The output is deterministic: the same inputs give the same files.

Run from the process directory of a processed checkout (with the output of
process.py), for example:

    python build_ontology.py ../bdqffdq --output-dir /tmp/bdqffdq-ontology
    python build_ontology.py ../bdqffdq --output-dir /tmp/out --robot /path/to/robot.jar

Requires rdflib. ROBOT needs Java 11 or later.
"""
import argparse, csv, datetime, json, os, pathlib, shutil, subprocess, sys, tempfile
import rdflib
from rdflib import BNode, Literal, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

# Annotation properties that OWL 2 DL does not allow, and what replaces them.
SUBSTITUTIONS = {RDF.value: SKOS.notation}

# Predicates with OWL meaning (not annotations); everything else is declared an
# owl:AnnotationProperty unless OWL 2 already defines it as one.
STRUCTURAL = {
    RDF.type, RDF.first, RDF.rest, RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range,
    OWL.equivalentClass, OWL.equivalentProperty, OWL.disjointWith, OWL.propertyDisjointWith,
    OWL.inverseOf, OWL.sameAs, OWL.differentFrom, OWL.onProperty, OWL.onClass, OWL.onDataRange,
    OWL.someValuesFrom, OWL.allValuesFrom, OWL.hasValue, OWL.hasSelf, OWL.cardinality,
    OWL.minCardinality, OWL.maxCardinality, OWL.qualifiedCardinality, OWL.minQualifiedCardinality,
    OWL.maxQualifiedCardinality, OWL.unionOf, OWL.intersectionOf, OWL.complementOf, OWL.oneOf,
    OWL.members, OWL.distinctMembers, OWL.disjointUnionOf, OWL.propertyChainAxiom, OWL.hasKey,
    OWL.versionIRI, OWL.imports, OWL.withRestrictions, OWL.onDatatype, OWL.datatypeComplementOf,
}
BUILTIN_ANNOTATIONS = {
    RDFS.label, RDFS.comment, RDFS.seeAlso, RDFS.isDefinedBy, OWL.deprecated, OWL.versionInfo,
    OWL.priorVersion, OWL.backwardCompatibleWith, OWL.incompatibleWith,
}
# The OWL 2 datatype map (OWL 2 Structural Specification, Section 4).
OWL2_DATATYPES = {RDF.PlainLiteral, RDF.XMLLiteral, RDFS.Literal, OWL.real, OWL.rational, RDF.langString} | {
    XSD[t] for t in ('decimal integer nonNegativeInteger nonPositiveInteger positiveInteger negativeInteger long int '
                     'short byte unsignedLong unsignedInt unsignedShort unsignedByte double float string '
                     'normalizedString token language Name NCName NMTOKEN boolean hexBinary base64Binary anyURI '
                     'dateTime dateTimeStamp').split()}


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def fail(message):
    sys.exit('build_ontology: ' + message)


class Expander:
    """Expands CURIEs with the dataset's namespace.csv, as the serializer does."""
    def __init__(self, namespace_csv):
        self.prefixes = {r['curie']: r['value'] for r in read_csv(namespace_csv)}

    def __call__(self, value):
        if value.startswith(('http://', 'https://', 'urn:')):
            return URIRef(value)
        prefix, sep, local = value.partition(':')
        if not sep or prefix not in self.prefixes:
            fail(f'cannot expand {value!r}: prefix not in namespace.csv')
        return URIRef(self.prefixes[prefix] + local)


def term_statements(dataset, graph):
    """Statements about the current terms, from the CSV and its column mappings."""
    name = dataset.name
    constants = read_csv(dataset / 'constants.csv')[0]
    mappings = read_csv(dataset / f'{name}-column-mappings.csv')
    expand = Expander(dataset / 'namespace.csv')
    root, key = constants['domainRoot'], constants['baseIriColumn']
    terms = set()
    for row in read_csv(dataset / constants['coreClassFile']):
        subject = URIRef(root + row[key])
        terms.add(subject)
        for m in mappings:
            if m['subject_id'] != '$root':
                continue        # linked resources (versions, replacements) are not part of the ontology
            if m['header'] == '$constant':
                value = m['value']
            elif m['header'] in row and row[m['header']].strip():
                value = row[m['header']].strip()
            else:
                continue
            predicate, kind = expand(m['predicate'].strip()), m['type']
            if kind == 'iri':
                obj = expand(m['value'] + value + m['attribute']) if m['value'] and m['header'] != '$constant' else expand(value)
            elif kind == 'language':
                obj = Literal(value, lang=m['attribute'])
            elif kind == 'datatype':
                obj = Literal(value, datatype=expand(m['attribute']))
            elif kind == 'plain':
                obj = Literal(value)
            else:
                continue
            graph.add((subject, predicate, obj))
    return root, terms


def vocabulary_header(repo, term_list):
    """The vocabulary that contains the term list, and its current version."""
    members = [r['vocabulary'] for r in read_csv(repo / 'vocabularies/vocabularies-members.csv') if r['termList'] == term_list]
    if len(members) != 1:
        fail(f'term list {term_list} is in {len(members)} vocabularies; expected 1')
    vocabulary = members[0]
    record = next(r for r in read_csv(repo / 'vocabularies/vocabularies.csv') if r['vocabulary'] == vocabulary)
    versions = [r for r in read_csv(repo / 'vocabularies-versions/vocabularies-versions.csv') if r['vocabulary'] == vocabulary]
    if not versions:
        fail(f'no version of vocabulary {vocabulary}')
    version = max(versions, key=lambda r: r['version_issued'])
    return vocabulary, record, version


def build(dataset, repo, axioms_path):
    graph = rdflib.Graph()
    term_list, terms = term_statements(dataset, graph)
    namespace = term_list

    # Axioms file: everything except its own ontology header.
    axioms = rdflib.Graph().parse(axioms_path, format='turtle')
    extension_lists = set(axioms.subjects(RDF.type, OWL.Ontology))
    for s, p, o in axioms:
        if s in extension_lists:
            continue
        for node in (s, o):
            if isinstance(node, URIRef) and str(node).startswith(namespace) and node not in terms and node != URIRef(namespace):
                fail(f'{axioms_path.name} uses {node}, which is not a term in {dataset.name}/{dataset.name}.csv')
        graph.add((s, p, o))

    untyped = sorted(t for t in terms if (t, RDF.type, None) not in graph)
    if untyped:
        fail('terms without rdf:type: ' + ', '.join(str(t) for t in untyped[:10]))

    # Substitutions for reserved annotation properties.
    substituted = {}
    for reserved, replacement in SUBSTITUTIONS.items():
        for s, o in list(graph.subject_objects(reserved)):
            if isinstance(o, Literal):
                graph.remove((s, reserved, o))
                graph.add((s, replacement, o))
                substituted[reserved] = replacement

    # Ontology header from the vocabulary record.
    vocabulary, record, version = vocabulary_header(repo, term_list)
    ontology = URIRef(vocabulary)
    graph.add((ontology, RDF.type, OWL.Ontology))
    graph.add((ontology, OWL.versionIRI, URIRef(version['version'])))
    graph.add((ontology, RDFS.label, Literal(record['label'], lang='en')))
    if record.get('description'):
        graph.add((ontology, DCTERMS.description, Literal(record['description'], lang='en')))
    if record.get('dc_creator'):
        graph.add((ontology, DCTERMS.creator, Literal(record['dc_creator'])))
    if record.get('dcterms_license'):
        graph.add((ontology, DCTERMS.license, URIRef(record['dcterms_license'])))
    graph.add((ontology, DCTERMS.issued, Literal(version['version_issued'], datatype=XSD.date)))
    for part in sorted({URIRef(term_list)} | extension_lists):
        graph.add((ontology, DCTERMS.hasPart, part))
    note = ('Generated by rs.tdwg.org process/build_ontology.py from the term list ' + term_list +
            (' and the vocabulary extension term list ' + ', '.join(sorted(str(e) for e in extension_lists)) if extension_lists else '') + '.')
    if substituted:
        names = {RDF.value: 'rdf:value', SKOS.notation: 'skos:notation'}
        note += ' For OWL 2 DL, ' + '; '.join(f'{names.get(k, k)} is replaced by {names.get(v, v)}' for k, v in sorted(substituted.items())) + \
                ' (rs.tdwg.org uses rdf:value for controlled value strings, TDWG Standards Documentation Specification 4.5.4).'
    graph.add((ontology, RDFS.comment, Literal(note, lang='en')))

    # Declarations.
    annotation_properties = {p for _, p, _ in graph} - STRUCTURAL - BUILTIN_ANNOTATIONS
    annotation_properties -= {s for s in graph.subjects(RDF.type, OWL.ObjectProperty)} | {s for s in graph.subjects(RDF.type, OWL.DatatypeProperty)}
    for p in annotation_properties:
        graph.add((p, RDF.type, OWL.AnnotationProperty))
    datatypes = {o.datatype for o in graph.objects() if isinstance(o, Literal) and o.datatype} | \
                {o for o in graph.objects(None, RDFS.range) if isinstance(o, URIRef) and str(o).startswith(str(XSD))}
    for d in datatypes - OWL2_DATATYPES:
        graph.add((d, RDF.type, RDFS.Datatype))
    return graph, ontology


def canonical(graph):
    """A copy of graph with deterministic blank node labels."""
    copy = rdflib.Graph()
    for triple in sorted(to_canonical_graph(graph)):    # sorted insertion: serializers follow insertion order
        copy.add(triple)
    return copy


def rdf11(graph):
    """A copy of graph in which xsd:string literals are plain literals (the same literal in RDF 1.1)."""
    copy = rdflib.Graph()
    for s, p, o in graph:
        if isinstance(o, Literal) and o.datatype == XSD.string:
            o = Literal(str(o))
        copy.add((s, p, o))
    return copy


def bind_prefixes(graph, dataset):
    for r in read_csv(dataset / 'namespace.csv'):
        graph.bind(r['curie'], r['value'], override=True, replace=True)


def write_rdflib(graph, out, name):
    graph.serialize(out / f'{name}.ttl', format='turtle')
    graph.serialize(out / f'{name}.rdf', format='xml')     # pretty-xml drops statements on list nodes


def sorted_json(value):
    """JSON-LD with nodes and value arrays in a fixed order (arrays of values are unordered sets)."""
    if isinstance(value, dict):
        return {k: sorted_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted((sorted_json(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value


def write_jsonld(graph, path):
    data = sorted_json(json.loads(graph.serialize(format='json-ld')))
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')


def find_robot(option):
    if option:
        return ['java', '-jar', option] if option.endswith('.jar') else [option]
    if os.environ.get('ROBOT_JAR'):
        return ['java', '-jar', os.environ['ROBOT_JAR']]
    if shutil.which('robot'):
        return ['robot']
    return None


def run_robot(robot, args):
    result = subprocess.run(robot + args, capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def main():
    # Some rdflib serializers iterate over sets, so their order depends on the string hash
    # seed; a fixed seed makes the output deterministic.
    if os.environ.get('PYTHONHASHSEED') != '0':
        os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED='0'))
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('dataset', help='dataset directory of the term list, e.g. ../bdqffdq')
    parser.add_argument('--axioms', help='axioms file (default: <dataset>/<dataset>-axioms.ttl)')
    parser.add_argument('--output-dir', required=True, help='directory for <dataset>.ttl, .rdf, and .jsonld')
    parser.add_argument('--robot', help='ROBOT executable or robot.jar (default: $ROBOT_JAR, or robot on PATH)')
    parser.add_argument('--no-robot', action='store_true', help='do not validate with ROBOT')
    args = parser.parse_args()

    dataset = pathlib.Path(args.dataset).resolve()
    repo = dataset.parent
    name = dataset.name
    axioms_path = pathlib.Path(args.axioms) if args.axioms else dataset / f'{name}-axioms.ttl'
    out = pathlib.Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    graph, ontology = build(dataset, repo, axioms_path)
    graph = canonical(graph)
    bind_prefixes(graph, dataset)
    write_rdflib(graph, out, name)

    robot = None if args.no_robot else find_robot(args.robot)
    if robot is None:
        write_jsonld(graph, out / f'{name}.jsonld')
        print(f'{ontology}: {len(graph)} triples written to {out}/{name}.{{ttl,rdf,jsonld}}.')
        print('NOT VALIDATED: ROBOT was not found, so the OWL 2 DL profile and consistency were not checked.')
        return

    source = out / f'{name}.ttl'
    code, text = run_robot(robot, ['validate-profile', '--input', str(source), '--profile', 'DL'])
    if code != 0:
        fail('not OWL 2 DL:\n' + text)
    with tempfile.TemporaryDirectory() as tmp:
        code, text = run_robot(robot, ['reason', '--input', str(source), '--reasoner', 'HermiT',
                                       '--output', str(pathlib.Path(tmp) / 'reasoned.owl')])
        if code != 0:
            fail('reasoner (HermiT) reports a problem:\n' + text)
    # Turtle and RDF/XML written by the OWL API.
    for fmt, ext in (('ttl', 'ttl'), ('owl', 'rdf')):
        target = out / f'{name}.{ext}'
        code, text = run_robot(robot, ['convert', '--input', str(source), '--format', fmt, '--output', str(target) + '.tmp'])
        if code != 0:
            fail(f'ROBOT convert to {fmt} failed:\n' + text)
        os.replace(str(target) + '.tmp', target)
    final = rdflib.Graph().parse(out / f'{name}.ttl', format='turtle')
    if not rdflib.compare.isomorphic(rdf11(final), rdf11(graph)):
        both, only_api, only_rdflib = rdflib.compare.graph_diff(rdflib.compare.to_isomorphic(rdf11(final)), rdflib.compare.to_isomorphic(rdf11(graph)))
        print(f'note: the OWL API serialization differs from the generated graph: {len(only_api)} statements added, {len(only_rdflib)} removed.')
    final = canonical(final)
    bind_prefixes(final, dataset)
    write_jsonld(final, out / f'{name}.jsonld')
    print(f'{ontology}: {len(final)} triples written to {out}/{name}.{{ttl,rdf,jsonld}}.')
    print('VALIDATED with ROBOT: OWL 2 DL profile, consistent (HermiT).')


if __name__ == '__main__':
    main()
