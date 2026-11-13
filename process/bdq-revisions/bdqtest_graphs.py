"""Generate the graph of each bdqtest version, for rs.tdwg.org to append to its RDF.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340); the BDQ step of option T3 (plan,
tdwg/bdq tg2/_make_review/deployment_rs_tdwg_org.md, Sections 10 and 10.9.2). Run on
the bdq branch after processing, like the copy of the mapping files.

A Test is defined by its whole graph (plan 10.9.1): the Test version and the nodes
that describe it (resource type, dimension, criterion or enhancement, information
elements, references), its Method, Specification, and Arguments, and each Policy that
includes it, with only this Test's includedInPolicy. For every version in
bdqtest-versions/bdqtest-versions.csv this script builds that graph with the pinned
builder (bdqtest_rdf.py) from the version's own row, and writes it, once, to

    bdqtest/graphs/<uuid>-<date>.ttl, .rdf, .jsonld

Labels that depend on the other Tests (the aggregated-response information elements,
the number of Tests in each Policy) are taken from the Tests current on the version's
date. The GUID tables are those of the latest release directory on or before the
version's date that contains bdqtest-graph-inputs/<table>.

bdqtest/bdqtest-graphs.csv gives the graph of each version IRI, and of each term IRI
(its current version's), for html/restxq.xqm to append to their RDF.

A Policy's label gives its number of Tests ("ValidationPolicy: (50) validations ..."), so it
is the label as of the version's date: a graph is written once and not changed when the
Policy grows.

Check: the graphs of the current versions together equal the graph of all current Tests
built at once, apart from the Policy labels of current versions issued before the Policy
last grew.

Requires rdflib. Usage, from the process directory:
    python bdqtest_graphs.py ..
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


versions = read_rows(root / 'bdqtest-versions' / 'bdqtest-versions.csv')
lookup = []
current_graphs = {}
latest = max(v['version_issued'] for v in versions)
_contexts = {}
for version in sorted(versions, key=lambda v: (v['version_issued'], v['version'])):
    date = version['version_issued']
    if date not in _contexts:
        _contexts[date] = context([published(v) for v in snapshot(versions, date)])
    labels, sizes = _contexts[date]
    graph = build([published(version)], date, labels, sizes)
    local = version['version'][len(NS + 'version/'):]
    write(graph, GRAPHS / local)
    files = f'bdqtest/graphs/{local}'
    lookup.append([version['version'], files])
    if version['version_status'] == 'recommended':
        lookup.append([NS + version['term_localName'], files])
        current_graphs[version['term_localName']] = graph

with open(root / 'bdqtest' / 'bdqtest-graphs.csv', 'w', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerows([['iri', 'graph']] + sorted(lookup))

# Check: the current versions' graphs together are the graph of all current Tests.
current_rows = [published(v) for v in snapshot(versions, latest)]
labels, sizes = context(current_rows)
whole = build(current_rows, latest, labels, sizes)
union = rdflib.Graph()
for graph in current_graphs.values():
    for triple in graph:
        union.add(triple)
RDFS, SKOS = rdflib.RDFS, rdflib.namespace.SKOS
POLICY_CLASSES = {bdqtest_rdf.BDQFFDQ[c] for c in ('ValidationPolicy', 'IssuePolicy', 'MeasurementPolicy', 'AmendmentPolicy')}


def without_policy_labels(graph):
    policies = {s_ for s_, _, o_ in graph.triples((None, rdflib.RDF.type, None)) if o_ in POLICY_CLASSES}
    out = rdflib.Graph()
    for s_, p_, o_ in graph:
        if not (s_ in policies and p_ in (RDFS.label, SKOS.prefLabel)):
            out.add((s_, p_, o_))
    return out


if not isomorphic(without_policy_labels(union), without_policy_labels(whole)):
    sys.exit(f'the current versions\' graphs ({len(union)} triples) differ from the whole graph ({len(whole)} triples)')
earlier_labels = len(union) - len(whole)
print(f'bdqtest graphs: {len(versions)} versions, {len(current_graphs)} current; current graphs together equal '
      f'the whole graph ({len(whole)} triples), apart from {earlier_labels} earlier Policy label(s)')
