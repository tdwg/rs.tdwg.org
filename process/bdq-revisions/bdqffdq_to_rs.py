"""Convert the BDQ bdqffdq ontology to rs.tdwg.org release inputs.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340). Like bdq_to_rs.py, this is a
one-way bootstrap from the files in tdwg/bdq, used to create the inputs for the
public review at bdq-public-review.rs.tdwg.org. It is not part of the
rs.tdwg.org processing workflow and is intended to be replaced: once the
bdqffdq inputs live authoritatively in this repository (the release-input CSV,
the axioms file and the mapping files under process/bdq-revisions/), those
files are edited directly and this script is no longer run. Don't run it over
inputs that have since been edited by hand, since it rewrites them.

Option C of the plan (tdwg/bdq tg2/_make_review/deployment_rs_tdwg_org.md,
Sections 9.3 and 9.5): the statements about named terms become a term list
(one row per term), and what cannot be rows (the ontology header, the
owl:Restriction ranges, the owl:AllDisjointClasses axioms) goes into a
parallel axioms file, a vocabulary extension term list in the sense of the
TDWG Standards Documentation Specification, Section 4.4.2.2.
process/build_ontology.py combines the two into the ontology.

Reads   <bdq>/tg2/_review/vocabulary/bdqffdq.owl (Turtle)
        <rs>/process/files_for_new/{current_terms,versions}/simple-vocabulary*-column-mappings.csv
Writes  <rs>/process/bdq-revisions/bdq-revisions-<date_issued>/
            bdqffdq.csv                     release-input CSV
            bdqffdq-axioms.ttl              axioms file
            mappings/bdqffdq/...            column mappings and namespace.csv
            mappings/bdqffdq-versions/...

Differences from bdqffdq.owl, by design (plan Section 9.5):
- per-term dcterms:issued is replaced by the dcterms:created/modified and term
  versions that process.py generates;
- the ontology's owl:versionIRI and dcterms:issued are set by build_ontology.py
  from the term list version;
- annotation property and datatype declarations are made by build_ontology.py;
- definitions are language-tagged @en throughout (a few are plain in the source).
The script checks that every other triple of bdqffdq.owl is reproduced.

Requires rdflib. Usage: python -I bdqffdq_to_rs.py <bdq_repo> <rs_repo> <date_issued>
"""
import csv, sys, pathlib, collections
import rdflib
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS, XSD

bdq, rs, date_issued = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
release_dir = rs / 'process' / f'bdq-revisions/bdq-revisions-{date_issued}'
NS = 'https://rs.tdwg.org/bdqffdq/terms/'
ONTOLOGY = URIRef('https://rs.tdwg.org/bdqffdq/terms')
source = bdq / 'tg2/_review/vocabulary/bdqffdq.owl'

g = rdflib.Graph().parse(source, format='turtle')

# Repeated columns: (base header, predicate, how many). Values are full IRIs.
REPEATED = [
    ('type', RDF.type, 2),
    ('subClassOf', RDFS.subClassOf, 3),
    ('subPropertyOf', RDFS.subPropertyOf, 4),
    ('range', RDFS.range, 1),
    ('differentFrom', OWL.differentFrom, 2),
]
def headers(base, n):
    return [base] + [f'{base}{i}' for i in range(1, n)]

LITERAL_COLUMNS = [
    ('label', RDFS.label), ('prefLabel', SKOS.prefLabel), ('definition', SKOS.definition),
    ('notes', SKOS.note), ('usage', SKOS.scopeNote), ('controlled_value_string', RDF.value),
]
HEADER = ['term_localName'] + [h for h, _ in LITERAL_COLUMNS] + \
         [h for base, _, n in REPEATED for h in headers(base, n)]

terms = sorted({s for s in g.subjects() if isinstance(s, URIRef) and str(s).startswith(NS)})
rows, axioms = [HEADER], rdflib.Graph()
axioms.bind('bdqffdq', NS); axioms.bind('owl', OWL); axioms.bind('skos', SKOS); axioms.bind('dcterms', DCTERMS)

def one(s, p):
    values = list(g.objects(s, p))
    if len(values) > 1:
        raise SystemExit(f'{s} has {len(values)} values of {p}')
    return str(values[0]).strip() if values else ''

for s in terms:
    row = {'term_localName': str(s)[len(NS):]}
    for h, p in LITERAL_COLUMNS:
        row[h] = one(s, p)
    if one(s, RDFS.comment) != row['definition']:
        raise SystemExit(f'{s}: rdfs:comment differs from skos:definition')
    for base, p, n in REPEATED:
        values = sorted(str(o) for o in g.objects(s, p) if isinstance(o, URIRef))
        if len(values) > n:
            raise SystemExit(f'{s}: {len(values)} values of {p}, more than {n} columns')
        for h, v in zip(headers(base, n), values + [''] * n):
            row[h] = v
    rows.append([row[h] for h in HEADER])

# Axioms file: the ontology header (except owl:versionIRI and dcterms:issued) and
# every statement with a blank node, i.e. the restriction ranges and disjointness axioms.
def add_bnode_closure(node):
    for p, o in g.predicate_objects(node):
        axioms.add((node, p, o))
        if isinstance(o, BNode):
            add_bnode_closure(o)
for p, o in g.predicate_objects(ONTOLOGY):
    if p not in (OWL.versionIRI, DCTERMS.issued):
        axioms.add((ONTOLOGY, p, o))
for s, p, o in g:
    if isinstance(s, URIRef) and isinstance(o, BNode):
        axioms.add((s, p, o)); add_bnode_closure(o)
    elif isinstance(s, BNode) and not any(True for _ in g.subjects(None, s)):
        axioms.add((s, p, o)); add_bnode_closure(s)   # unreferenced root, e.g. owl:AllDisjointClasses

# Check: CSV triples + axioms + declarations reproduce bdqffdq.owl, apart from the documented differences.
rebuilt = rdflib.Graph()
for t in axioms: rebuilt.add(t)
for r in rows[1:]:
    s = URIRef(NS + r[0]); row = dict(zip(HEADER, r))
    for h, p in LITERAL_COLUMNS:
        if row[h]: rebuilt.add((s, p, Literal(row[h])))
    for base, p, n in REPEATED:
        for h in headers(base, n):
            if row[h]: rebuilt.add((s, p, URIRef(row[h])))
def normalized(graph):
    out = set()
    for s, p, o in graph:
        if p == DCTERMS.issued or (s == ONTOLOGY and p == OWL.versionIRI): continue
        if p == RDF.type and o in (OWL.AnnotationProperty, RDFS.Datatype) and not str(s).startswith(NS): continue
        if p == RDFS.comment and isinstance(s, URIRef) and str(s).startswith(NS): continue
        if isinstance(o, Literal): o = Literal(str(o).strip())   # language tags and whitespace normalized
        out.add((s, p, o))
    return out
a, b = normalized(g), normalized(rebuilt)
named = lambda ts: {t for t in ts if not any(isinstance(x, BNode) for x in t)}
if named(a) != named(b):
    raise SystemExit(f'not reproduced: {sorted(named(a) - named(b))[:5]} / extra: {sorted(named(b) - named(a))[:5]}')
if len(a) != len(b) or len(a - named(a)) != len(b - named(b)):
    raise SystemExit('blank-node statements not reproduced')

release_dir.mkdir(parents=True, exist_ok=True)
with open(release_dir / 'bdqffdq.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerows(rows)
header_comment = ('# bdqffdq axioms: a vocabulary extension term list (TDWG Standards Documentation\n'
                  '# Specification, Section 4.4.2.2). Statements that cannot be rows of bdqffdq.csv: the\n'
                  '# ontology header, the owl:Restriction ranges, and the owl:AllDisjointClasses axioms.\n'
                  '# process/build_ontology.py combines this file with the term list into the ontology,\n'
                  '# and adds owl:versionIRI, dcterms:issued, and the declarations.\n')
(release_dir / 'bdqffdq-axioms.ttl').write_text(header_comment + axioms.serialize(format='turtle'), encoding='utf-8')

# Column mappings: the simple vocabulary (vocab_type 1) templates, edited.
def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))
def write_csv(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, lineterminator='\n').writerows(data)
EXTRA = [
    ['controlled_value_string', 'rdf:value', 'plain', '', '', '$root'],      # SDS 4.5.4
    ['controlled_value_string', 'skos:notation', 'plain', '', '', '$root'],  # the same string, for OWL 2 DL (plan 9.5)
] + [[h, 'rdf:type' if base == 'type' else {'subClassOf': 'rdfs:subClassOf', 'subPropertyOf': 'rdfs:subPropertyOf',
       'range': 'rdfs:range', 'differentFrom': 'owl:differentFrom'}[base], 'iri', '', '', '$root']
     for base, _, n in REPEATED for h in headers(base, n) if h != 'type']
for kind, template, target, dest in (
    ('current_terms', 'simple-vocabulary-column-mappings.csv', 'bdqffdq-column-mappings.csv', 'bdqffdq'),
    ('versions', 'simple-vocabulary-versions-column-mappings.csv', 'bdqffdq-versions-column-mappings.csv', 'bdqffdq-versions'),
):
    template_rows = read_csv(rs / 'process/files_for_new' / kind / template)
    out = [template_rows[0]]
    for row in template_rows[1:]:
        h, pred = row[0], row[1]
        if h == 'label' and pred == 'skos:prefLabel':
            row = ['prefLabel', 'skos:prefLabel', 'language', '', 'en', '$root']
        elif h == 'usage':
            row = ['usage', 'skos:scopeNote', 'datatype', '', 'xsd:string', '$root']
        elif h == 'notes':
            row = ['notes', 'skos:note', 'language', '', 'en', '$root']
        elif h == 'term_localName':        # versions: dcterms:isVersionOf
            row = row[:3] + [NS] + row[4:]
        elif h == 'tdwgutility_organizedInClass':
            continue
        out.append(row)
        if h == 'type':
            out.extend(EXTRA)
    write_csv(release_dir / 'mappings' / dest / target, out)
    ns_rows = read_csv(rs / 'process/files_for_new' / kind / 'namespace.csv')
    if not any(r and r[0] == 'bdqffdq' for r in ns_rows):
        ns_rows.append(['bdqffdq', NS])
    write_csv(release_dir / 'mappings' / dest / 'namespace.csv', ns_rows)

counts = collections.Counter(r[HEADER.index('type')].rsplit('#', 1)[-1] for r in rows[1:])
print(f'bdqffdq: {len(rows) - 1} terms {dict(counts)}; {len(axioms)} axiom triples; reproduces bdqffdq.owl')
