"""Generate the graphs of the bdqtest terms and versions, and the linked tables of the element term lists.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340); the BDQ step of option T3 (plan,
tdwg/bdq tg2/_make_review/deployment_rs_tdwg_org.md, Sections 10, 10.9.2 and 10.9.9). Run on
the bdq branch after processing, like the copy of the mapping files.

A Test is defined by its whole graph (plan 10.9.1): the Test and the nodes that describe it
(resource type, dimension, criterion or enhancement, information elements, references), its
Method, Specification, and Arguments, and each Policy that includes it, with only this Test's
includedInPolicy. The graph is built with the pinned builder (bdqtest_rdf.py), in two forms
(plan 10.9.9):

- the current graph of each Test term, between current resources: the Test bdqtest:<uuid>, its
  Method https://rs.tdwg.org/bdqtest/method/<uuid>, and so on, each owl:sameAs its bare
  urn:uuid:; written to bdqtest/graphs/<uuid>.{ttl,rdf,jsonld};
- the graph of each Test version, between versions: the Test version, and the versions of its
  Method, Specification, Arguments, information elements, and Policies current on its date
  (from the element term lists' versions, processed by process.py from the inputs that
  bdqtest_elements_to_rs.py derives), each dcterms:isVersionOf its current element; written,
  once, to bdqtest/graphs/<uuid>-<date>.{ttl,rdf,jsonld}.

Labels that depend on the other Tests (the aggregated-response information elements, the number
of Tests in each Policy) are taken from the Tests current on the version's date, for a version,
and from the current Tests, for a term. The GUID tables are those of the latest release directory
on or before that date that contains bdqtest-graph-inputs/<table>.

bdqtest/bdqtest-graphs.csv gives the graph of each term IRI and version IRI, for html/restxq.xqm
to append to their RDF.

It also writes, for the element term lists:
- the linked tables of the links with many values, from the '|'-separated columns that
  bdqtest_elements_to_rs.py carries: bdqtestpolicy{,-versions}/...-members.csv (includedInPolicy)
  and bdqtestinformationelement{,-versions}/...-composedof.csv (composedOf);
- <dataset>/<dataset>-redirects.csv, where html/restxq.xqm redirects an element requested as HTML:
  a Method, Specification, or Argument to its Test's anchor in the bdqtest List of Terms, a Policy
  to its Use Case's anchor in the bdquc List of Terms; an information element (most are shared
  between Tests) has no redirect, and gets rs.tdwg.org's own term page.

Check: the current graphs of the Tests together equal the current graph of all current Tests
built at once.

With --whole DIR, it writes instead the current graph of all current Tests, with the statements
that support the ontology (class declarations and hierarchy of the nodes used), as
DIR/bdqtest.{ttl,rdf,jsonld}, and writes nothing else. This is the whole-vocabulary serialization that
tdwg/bdq publishes in tg2/_review/dist/ (its export_rs_baseline.py runs this from a pinned commit), so
both repositories use the same builder (deployment_rs_tdwg_org.md Section 13.1).

Requires rdflib. Usage, from the process directory:
    python bdqtest_graphs.py ..
    python bdqtest_graphs.py .. --whole <output directory>
"""
import csv, os, pathlib, sys

if os.environ.get('PYTHONHASHSEED') != '0':
    # rdflib's RDF/XML and JSON-LD writers iterate over sets: fix the seed so the files are reproducible.
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED='0'))

import json  # noqa: E402
import rdflib  # noqa: E402
from rdflib.compare import isomorphic  # noqa: E402

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import bdqtest_rdf  # noqa: E402
from bdqtest_columns import COLUMNS  # noqa: E402

root = pathlib.Path(sys.argv[1]).resolve()
WHOLE = pathlib.Path(sys.argv[sys.argv.index('--whole') + 1]).resolve() if '--whole' in sys.argv else None
NS = 'https://rs.tdwg.org/bdqtest/terms/'
GRAPHS = root / 'bdqtest' / 'graphs'
TABLES = {
    'additional': 'TG2_tests_additional_guids.csv',
    'ie': 'information_element_guids.csv',
    'policy': 'TG2_policy_guids.csv',
    'citation': 'TG2_citation_guids.csv',
}
TO_PUBLISHED = {rs_name: name for name, rs_name in COLUMNS.items() if rs_name}


def read_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


releases = sorted(p for p in (here).glob('bdq-revisions-20*') if p.is_dir())


def table(name, date):
    """The GUID table of the latest release on or before date that has one."""
    found = [p / 'bdqtest-graph-inputs' / name for p in releases
             if p.name[len('bdq-revisions-'):] <= date and (p / 'bdqtest-graph-inputs' / name).exists()]
    if not found:
        sys.exit(f'no {name} on or before {date}')
    return str(found[-1])


_tables = {}


def tables(date):
    key = tuple(table(name, date) for name in TABLES.values())
    if key not in _tables:
        additional, ie, policy, citation = key
        _tables[key] = (bdqtest_rdf.load_additional_guids(additional), bdqtest_rdf.load_ie_guids(ie),
                        bdqtest_rdf.load_policy_guids(policy), bdqtest_rdf.load_citation_guids(citation))
    return _tables[key]


def published(version):
    """A bdqtest version row in the column names of bdqtest_term_versions.csv."""
    row = {TO_PUBLISHED[k]: v for k, v in version.items() if k in TO_PUBLISHED}
    row['issued'] = version['version_issued']
    row['term_iri'] = NS + version['term_localName']
    return row


def snapshot(versions, date):
    """The version of each Test current on date."""
    current = {}
    for v in versions:
        if v['version_issued'] <= date:
            if v['term_localName'] not in current or v['version_issued'] > current[v['term_localName']]['version_issued']:
                current[v['term_localName']] = v
    return list(current.values())


def context(rows):
    labels = {r['term_iri']: r['Label'].strip() for r in rows}
    sizes = {}
    for r in rows:
        policy_type = bdqtest_rdf._test_type_to_policy_type(r['Type'].strip())
        for use_case in (u.strip() for u in r['UseCases'].split(',') if u.strip()):
            sizes[(use_case, policy_type)] = sizes.get((use_case, policy_type), 0) + 1
    return labels, sizes


def build(rows, date, labels, sizes):
    additional, ie, policy, citation = tables(date)
    return bdqtest_rdf.build_graph(rows, additional, ie, policy, citation, term_iri_to_label=labels,
                                   policy_sizes=sizes, ontology_support=False)


def ordered(value):
    if isinstance(value, dict):
        return {k: ordered(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted((ordered(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value


def write(graph, base):
    out = rdflib.Graph()
    for prefix, namespace in graph.namespaces():
        out.bind(prefix, namespace, override=True, replace=True)
    for triple in sorted(graph):
        out.add(triple)
    base.parent.mkdir(parents=True, exist_ok=True)
    out.serialize(str(base) + '.ttl', format='turtle')
    out.serialize(str(base) + '.rdf', format='xml')
    data = ordered(json.loads(out.serialize(format='json-ld')))
    with open(str(base) + '.jsonld', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + '\n')


B = bdqtest_rdf.BDQFFDQ
DCT, OWL = rdflib.namespace.DCTERMS, rdflib.OWL
KINDS = ['method', 'specification', 'argument', 'informationelement', 'policy']
ENS = {k: f'https://rs.tdwg.org/bdqtest/{k}/' for k in KINDS}
KIND_OF_CLASS = {B[c]: 'method' for c in ('ValidationMethod', 'MeasurementMethod', 'AmendmentMethod', 'IssueMethod')}
KIND_OF_CLASS.update({B.Specification: 'specification', B.Argument: 'argument', B.ActedUpon: 'informationelement',
                      B.Consulted: 'informationelement'})
KIND_OF_CLASS.update({B[c]: 'policy' for c in ('ValidationPolicy', 'MeasurementPolicy', 'AmendmentPolicy', 'IssuePolicy')})


def element_nodes(graph):
    """The urn:uuid: nodes of the elements, with their kind (not the bibliographic resources)."""
    nodes = {}
    for s, o in graph.subject_objects(rdflib.RDF.type):
        if str(s).startswith('urn:uuid:') and o in KIND_OF_CLASS:
            nodes[s] = KIND_OF_CLASS[o]
    return nodes


def renamed(graph, mapping):
    out = rdflib.Graph()
    for prefix, namespace in graph.namespaces():
        out.bind(prefix, namespace, override=True, replace=True)
    for s, p, o in graph:
        out.add((mapping.get(s, s), p, mapping.get(o, o)))
    return out


# The versions of each element, from the processed element term lists.
element_dates = {k: {} for k in KINDS}
for kind in KINDS:
    for row in read_rows(root / f'bdqtest{kind}-versions' / f'bdqtest{kind}-versions.csv'):
        local = row['versionLocalName']
        element_dates[kind].setdefault(local[:-11], []).append(local[-10:])


def element_version(kind, uuid, date):
    found = [d for d in element_dates[kind].get(uuid, []) if d <= date]
    if not found:
        sys.exit(f'no version of {kind} {uuid} on or before {date}')
    return rdflib.URIRef(f'{ENS[kind]}version/{uuid}-{max(found)}')


def versioned(graph, date):
    """A Test version's graph, between the versions of its elements current on date."""
    nodes = element_nodes(graph)
    mapping = {n: element_version(k, str(n)[9:], date) for n, k in nodes.items()}
    out = renamed(graph, mapping)
    for n, k in nodes.items():
        out.add((mapping[n], DCT.isVersionOf, rdflib.URIRef(ENS[k] + str(n)[9:])))
    return out


def current_form(graph, tests):
    """The current graph of Tests (term local name -> date of the version built), between current resources."""
    nodes = element_nodes(graph)
    mapping = {n: rdflib.URIRef(ENS[k] + str(n)[9:]) for n, k in nodes.items()}
    terms = {}
    for local, date in tests.items():
        terms[rdflib.URIRef(f'{NS}version/{local}-{date}')] = rdflib.URIRef(NS + local)
    mapping.update(terms)
    out = renamed(graph, mapping)
    for term in terms.values():
        out.remove((term, DCT.isVersionOf, None))
        out.remove((term, DCT.issued, None))
        out.add((term, OWL.sameAs, rdflib.URIRef('urn:uuid:' + str(term)[len(NS):])))
    for n in nodes:
        out.add((mapping[n], OWL.sameAs, n))
    out.bind('owl', OWL)
    return out


versions = read_rows(root / 'bdqtest-versions' / 'bdqtest-versions.csv')
latest = max(v['version_issued'] for v in versions)
current_versions = snapshot(versions, latest)
current_rows = [published(v) for v in current_versions]
current_dates = {v['term_localName']: v['version_issued'] for v in current_versions}
labels, sizes = context(current_rows)
if WHOLE:
    # The current graph of all current Tests, with the ontology-support statements.
    additional, ie, policy, citation = tables(latest)
    whole = bdqtest_rdf.build_graph(current_rows, additional, ie, policy, citation, term_iri_to_label=labels,
                                    policy_sizes=sizes, ontology_support=True)
    whole = current_form(whole, current_dates)
    write(whole, WHOLE / 'bdqtest')
    print(f'bdqtest whole graph: {len(current_rows)} current Tests, {len(whole)} triples, in {WHOLE}/bdqtest.{{ttl,rdf,jsonld}}')
    sys.exit(0)

lookup = []
_contexts = {}
for version in sorted(versions, key=lambda v: (v['version_issued'], v['version'])):
    date = version['version_issued']
    if date not in _contexts:
        _contexts[date] = context([published(v) for v in snapshot(versions, date)])
    v_labels, v_sizes = _contexts[date]
    graph = versioned(build([published(version)], date, v_labels, v_sizes), date)
    local = version['version'][len(NS + 'version/'):]
    write(graph, GRAPHS / local)
    lookup.append([version['version'], f'bdqtest/graphs/{local}'])

current_graphs = {}
for version in current_versions:
    local = version['term_localName']
    graph = current_form(build([published(version)], latest, labels, sizes), {local: version['version_issued']})
    write(graph, GRAPHS / local)
    lookup.append([NS + local, f'bdqtest/graphs/{local}'])
    current_graphs[local] = graph

with open(root / 'bdqtest' / 'bdqtest-graphs.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerows([['iri', 'graph']] + sorted(lookup))

# Check: the current graphs of the Tests together are the current graph of all current Tests.
whole = current_form(build(current_rows, latest, labels, sizes), current_dates)
union = rdflib.Graph()
for graph in current_graphs.values():
    for triple in graph:
        union.add(triple)
if not isomorphic(union, whole):
    sys.exit(f'the current graphs of the Tests ({len(union)} triples) differ from the whole graph ({len(whole)} triples)')


# Linked tables of the element term lists, and their HTML redirects.
def write_rows(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)


for kind, column, suffix in (('policy', 'members', 'members'), ('informationelement', 'composedOf', 'composedof')):
    db = f'bdqtest{kind}'
    write_rows(root / db / f'{db}-{suffix}.csv', [['term_localName', 'object']] + sorted(
        [r['term_localName'], o] for r in read_rows(root / db / f'{db}.csv') for o in r[column].split('|') if o))
    version_column = 'memberVersions' if kind == 'policy' else column
    write_rows(root / f'{db}-versions' / f'{db}-versions-{suffix}.csv', [['versionLocalName', 'object']] + sorted(
        [r['versionLocalName'], o] for r in read_rows(root / f'{db}-versions' / f'{db}-versions.csv')
        for o in r[version_column].split('|') if o))

redirects = {r['database']: r for r in read_rows(root / 'html' / 'redirects.csv')}


def anchor(database, local):
    r = redirects[database]
    base = r['prefix'] + (r['namespace'] + r['connector'] if r['useNamespace'] == 'yes' else '')
    return base + local


for kind in KINDS:
    db = f'bdqtest{kind}'
    rows = []
    for r in read_rows(root / db / f'{db}.csv'):
        if kind == 'policy':
            target = anchor('bdquc', r['hasUseCase'].rsplit('/', 1)[-1])
        elif kind == 'informationelement':
            target = ''
        else:
            target = anchor('bdqtest', r['test'])
        rows.append([r['term_localName'], target])
    write_rows(root / db / f'{db}-redirects.csv', [['localName', 'redirect']] + sorted(rows))

print(f'bdqtest graphs: {len(versions)} versions and {len(current_graphs)} terms; the terms\' graphs together equal '
      f'the current graph of all current Tests ({len(whole)} triples); linked tables and redirects of the elements written')
