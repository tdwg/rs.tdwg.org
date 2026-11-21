"""Derive the release inputs of the bdqtest element term lists from the Test rows and GUID tables.

FOR THE BDQ PUBLIC REVIEW (tdwg/bdq#340); plan (tdwg/bdq tg2/_make_review/deployment_rs_tdwg_org.md)
Section 10.9.9. The structural nodes of the BDQ Tests are term lists of the bdqtest vocabulary,
processed by process.py like any TDWG term list (decided 2026-11-14):

    https://rs.tdwg.org/bdqtest/method/              bdqtestmethod
    https://rs.tdwg.org/bdqtest/specification/       bdqtestspecification
    https://rs.tdwg.org/bdqtest/argument/            bdqtestargument
    https://rs.tdwg.org/bdqtest/informationelement/  bdqtestinformationelement
    https://rs.tdwg.org/bdqtest/policy/              bdqtestpolicy

Each element keeps its UUID as local name, and states owl:sameAs its bare urn:uuid:. So do the Tests.

The element rows are DERIVED, not edited: from the bdqtest rows of each release (the Test's
Specification, Arguments, notes, information elements, Use Cases) and the GUID tables in force on
its date (process/bdq-revisions/*/bdqtest-graph-inputs/), with the pinned builder bdqtest_rdf.py, so
they agree with the Test graphs. To change an element, change the Test's row or a GUID table in a
release, and rerun this script; it rewrites the element inputs of every release.

Two forms of the links between elements (plan 10.9.9):
- the current form, between current resources (a Method forValidation bdqtest:<uuid>), mapped in the
  current-term datasets;
- the versioned form, between versions (forValidationVersion: the Test version of the same release),
  in columns mapped only in the -versions datasets.

An element gets a version in a release when its row changes there, its version links included, so
versions cascade upward as rs.tdwg.org does for terms and term lists: a changed Argument gives new
versions of its Specification, Method, and Test; every Test version gives a Method version; a Policy
gets a version whenever one of its Tests does. A changed Argument, Specification, or information
element without a version of its Tests in the same release is an error.

Links with many values (a Policy's Tests, an information element's composedOf terms) are carried as
'|'-separated columns and written as linked tables by bdqtest_graphs.py after processing.

Writes, in each release directory that declares bdqtest:
    bdqtest{method,specification,argument,informationelement,policy}.csv   (header only if no change)
    bdqtest.csv                     with the added columns (owl:sameAs, information element links),
                                    and methodGuid and specificationGuid from the GUID table
    config.yaml                     the five namespaces in the bdqtest vocabulary
and, in the first bdqtest release, mappings/<dataset>/ and mappings/<dataset>-versions/ for the
five datasets, and the added bdqtest mappings.

Requires rdflib and pyyaml. Usage, from process/: python bdq-revisions/bdqtest_elements_to_rs.py
"""
import csv, pathlib, sys
from collections import defaultdict

import yaml

here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import rdflib  # noqa: E402
import bdqtest_rdf  # noqa: E402
from bdqtest_columns import COLUMNS, HEADER  # noqa: E402

B = bdqtest_rdf.BDQFFDQ
RDF, RDFS, SKOS, DCT = rdflib.RDF, rdflib.RDFS, rdflib.namespace.SKOS, rdflib.namespace.DCTERMS
TNS = 'https://rs.tdwg.org/bdqtest/terms/'
KINDS = ['argument', 'specification', 'informationelement', 'method', 'policy']   # dependency order
NS = {k: f'https://rs.tdwg.org/bdqtest/{k}/' for k in KINDS}
PREFIX = {k: 'bdqtest' + k for k in KINDS}
TO_PUBLISHED = {rs_name: name for name, rs_name in COLUMNS.items() if rs_name}
GUID_TABLES = ['TG2_tests_additional_guids.csv', 'information_element_guids.csv', 'TG2_policy_guids.csv',
               'TG2_citation_guids.csv']
METHOD_CLASSES = {B[c] for c in ('ValidationMethod', 'MeasurementMethod', 'AmendmentMethod', 'IssueMethod')}
POLICY_CLASSES = {B[c] for c in ('ValidationPolicy', 'MeasurementPolicy', 'AmendmentPolicy', 'IssuePolicy')}
FOR = {B.forValidation: 'forValidation', B.forMeasure: 'forMeasure', B.forAmendment: 'forAmendment',
       B.forIssue: 'forIssue'}
CURIES = {'https://rs.tdwg.org/bdqffdq/terms/': 'bdqffdq:', 'https://rs.tdwg.org/bdqval/terms/': 'bdqval:',
          'http://rs.tdwg.org/dwc/terms/': 'dwc:', 'https://rs.tdwg.org/bdquc/terms/': 'bdquc:',
          'http://www.w3.org/ns/oa#': 'oa:'}

# Columns of each element dataset: (column, predicate, mapping type, attribute, in current, in versions).
# Columns with no predicate are carried (used to build linked tables and redirects), not mapped.
L, I, D, C = 'language', 'iri', 'datatype', None
COMMON = [('label', 'rdfs:label', L, 'en', 1, 1), ('type', 'rdf:type', I, '', 1, 1),
          ('sameAs', 'owl:sameAs', I, '', 1, 0)]
FIELDS = {
    'argument': COMMON + [
        ('argumentValue', 'bdqffdq:hasArgumentValue', D, 'xsd:string', 1, 1),
        ('hasParameter', 'bdqffdq:hasParameter', I, '', 1, 1),
        ('test', C, C, C, 0, 0)],
    'specification': COMMON + [
        ('description', 'dcterms:description', L, 'en', 1, 1),
        ('expectedResponse', 'bdqffdq:hasExpectedResponse', L, 'en', 1, 1),
        ('authoritiesDefaults', 'bdqffdq:hasAuthoritiesDefaults', L, 'en', 1, 1)]
        + [(f'example{n}', 'skos:example', L, 'en', 1, 1) for n in (1, 2, 3)]
        + [(f'hasArgument{n}', 'bdqffdq:hasArgument', I, '', 1, 0) for n in (1, 2, 3, 4)]
        + [(f'hasArgument{n}Version', 'bdqffdq:hasArgument', I, '', 0, 1) for n in (1, 2, 3, 4)]
        + [('test', C, C, C, 0, 0)],
    'informationelement': COMMON + [
        ('prefLabel', 'skos:prefLabel', L, 'en', 1, 1),
        ('definition', 'rdfs:comment', L, 'en', 1, 1),
        ('definition', 'skos:definition', L, 'en', 1, 1),
        ('note', 'skos:note', L, 'en', 1, 1),
        ('aggregatesResponsesFrom', 'bdqffdq:aggregatesResponsesFrom', I, '', 1, 1),
        ('composedOf', C, C, C, 0, 0)],
    'method': COMMON + [
        ('prefLabel', 'skos:prefLabel', L, 'en', 1, 1),
        ('historyNote', 'skos:historyNote', L, 'en', 1, 1)]
        + [(f'note{n}', 'skos:note', L, 'en', 1, 1) for n in (1, 2, 3)]
        + [(p, f'bdqffdq:{p}', I, '', 1, 0) for p in FOR.values()]
        + [(f'{p}Version', f'bdqffdq:{p}', I, '', 0, 1) for p in FOR.values()]
        + [('hasSpecification', 'bdqffdq:hasSpecification', I, '', 1, 0),
           ('hasSpecificationVersion', 'bdqffdq:hasSpecification', I, '', 0, 1),
           ('test', C, C, C, 0, 0)],
    'policy': COMMON + [
        ('prefLabel', 'skos:prefLabel', L, 'en', 1, 1),
        ('hasUseCase', 'bdqffdq:hasUseCase', I, '', 1, 1),
        ('members', C, C, C, 0, 0),
        ('memberVersions', C, C, C, 0, 0)],
}
# Columns added to the bdqtest rows, and their mappings.
TEST_FIELDS = [
    ('sameAs', 'owl:sameAs', I, '', 1, 0),
    ('hasActedUponInformationElement', 'bdqffdq:hasActedUponInformationElement', I, '', 1, 0),
    ('hasConsultedInformationElement', 'bdqffdq:hasConsultedInformationElement', I, '', 1, 0),
    ('hasActedUponInformationElementVersion', 'bdqffdq:hasActedUponInformationElement', I, '', 0, 1),
    ('hasConsultedInformationElementVersion', 'bdqffdq:hasConsultedInformationElement', I, '', 0, 1),
]
TEST_ADDED = [f[0] for f in TEST_FIELDS]
LABELS = {  # PROVISIONAL for the review, like the other BDQ term list labels and descriptions.
    'method': ('Data Quality Test Method terms', 'The Methods of the BDQ Tests, each linking a Test to its Specification.'),
    'specification': ('Data Quality Test Specification terms', 'The Specifications of the BDQ Tests.'),
    'argument': ('Data Quality Test Argument terms', 'The Arguments of the Specifications of the BDQ Tests: default values of their Parameters.'),
    'informationelement': ('Data Quality Test information element terms', 'The information elements that the BDQ Tests act upon or consult.'),
    'policy': ('Data Quality Test Policy terms', 'The Policies of the BDQ Use Cases: for each Use Case and type of Test, the Tests it includes.'),
}
NAMESPACES = [['bdqffdq', 'https://rs.tdwg.org/bdqffdq/terms/'], ['bdqval', 'https://rs.tdwg.org/bdqval/terms/'],
              ['bdquc', 'https://rs.tdwg.org/bdquc/terms/'], ['bdqtest', TNS]] + [[PREFIX[k], NS[k]] for k in KINDS]


def read_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)


def curie(iri):
    for ns, prefix in CURIES.items():
        if iri.startswith(ns):
            return prefix + iri[len(ns):]
    return iri


releases = sorted(p for p in here.glob('bdq-revisions-20*') if p.is_dir())
dates = [p.name[len('bdq-revisions-'):] for p in releases]


def table(name, date):
    found = [p / 'bdqtest-graph-inputs' / name for p, d in zip(releases, dates)
             if d <= date and (p / 'bdqtest-graph-inputs' / name).exists()]
    if not found:
        sys.exit(f'no {name} on or before {date}')
    return str(found[-1])


_tables = {}


def tables(date):
    key = tuple(table(n, date) for n in GUID_TABLES)
    if key not in _tables:
        a, i, p, c = key
        _tables[key] = (bdqtest_rdf.load_additional_guids(a), bdqtest_rdf.load_ie_guids(i),
                        bdqtest_rdf.load_policy_guids(p), bdqtest_rdf.load_citation_guids(c))
    return _tables[key]


def published(row, date):
    r = {TO_PUBLISHED[k]: v for k, v in row.items() if k in TO_PUBLISHED}
    r['issued'] = date
    r['term_iri'] = TNS + row['term_localName']
    return r


def uuid(node):
    s = str(node)
    if not s.startswith('urn:uuid:'):
        sys.exit(f'not a urn:uuid: node: {s}')
    return s[len('urn:uuid:'):]


def tversion(local, date):
    return f'{TNS}version/{local}-{date}'


def eversion(kind, local, date):
    return f'{NS[kind]}version/{local}-{date}'


test_rows = {d: read_rows(p / 'bdqtest.csv') for p, d in zip(releases, dates) if (p / 'bdqtest.csv').exists()}
first = min(test_rows)

snapshot = {}            # Test local name -> (date, row): the current version of each Test
test_version = {}        # Test local name -> date of its latest version
element_version = {}     # (kind, uuid) -> date of its latest version
emitted = {}             # (kind, uuid) -> the last row given a version
element_rows = {}        # date -> kind -> [rows]
problems = []

for date in dates:
    if date not in test_rows:
        continue
    rows = test_rows[date]
    for r in rows:
        snapshot[r['term_localName']] = (date, r)
        test_version[r['term_localName']] = date
    current = [published(r, d) for d, r in snapshot.values()]
    labels = {r['term_iri']: r['Label'].strip() for r in current}
    additional, ie_guids, policy_guids, citations = tables(date)
    g = bdqtest_rdf.build_graph([published(r, date) for r in rows], additional, ie_guids, policy_guids, citations,
                                term_iri_to_label=labels, ontology_support=False)
    whole = bdqtest_rdf.build_graph(current, additional, ie_guids, policy_guids, citations,
                                    term_iri_to_label=labels, ontology_support=False)

    def values(node, pred, graph=g):
        return sorted(str(o) for o in graph.objects(node, pred))

    def one(node, pred, graph=g):
        v = values(node, pred, graph)
        if len(v) > 1:
            sys.exit(f'{date}: {node} has {len(v)} values of {pred}')
        return v[0] if v else ''

    def kind_of(node, graph=g):
        return 'bdqffdq:' + str(next(graph.objects(node, RDF.type))).rsplit('/', 1)[-1]

    found = defaultdict(dict)
    owner = {}   # (kind, uuid) -> Test local name, for the elements that belong to one Test

    def add(kind, node, row):
        u = uuid(node)
        row = {'term_localName': u, 'sameAs': str(node), **row}
        if u in found[kind] and found[kind][u] != row:
            problems.append(f'{date}: {kind} {u} differs between the Tests of the release')
        found[kind][u] = row

    for s in set().union(*(g.subjects(RDF.type, c) for c in METHOD_CLASSES)):
        fors = [(FOR[p], str(o)) for p, o in g.predicate_objects(s) if p in FOR]
        test = fors[0][1][len(TNS + 'version/'):-len('-' + date)]
        spec = next(g.objects(s, B.hasSpecification))
        notes = values(s, SKOS.note)
        if len(notes) > 3:
            sys.exit(f'{date}: Method {s} has {len(notes)} notes')
        row = {'label': one(s, RDFS.label), 'prefLabel': one(s, SKOS.prefLabel), 'type': kind_of(s),
               'historyNote': one(s, SKOS.historyNote), 'test': test,
               'hasSpecification': NS['specification'] + uuid(spec)}
        row.update({f'note{n + 1}': notes[n] if n < len(notes) else '' for n in range(3)})
        row.update({p: (TNS + test if p == fors[0][0] else '') for p in FOR.values()})
        add('method', s, row)
        owner[('specification', uuid(spec))] = test
        for a in g.objects(spec, B.hasArgument):
            owner[('argument', uuid(a))] = test
    for s in set(g.subjects(RDF.type, B.Specification)):
        examples = values(s, SKOS.example)
        args = sorted(uuid(o) for o in g.objects(s, B.hasArgument))
        if len(examples) > 3 or len(args) > 4:
            sys.exit(f'{date}: Specification {s} has {len(examples)} examples and {len(args)} Arguments')
        row = {'label': one(s, RDFS.label), 'type': kind_of(s), 'description': one(s, DCT.description),
               'expectedResponse': one(s, B.hasExpectedResponse),
               'authoritiesDefaults': one(s, B.hasAuthoritiesDefaults), 'test': owner[('specification', uuid(s))]}
        row.update({f'example{n + 1}': examples[n] if n < len(examples) else '' for n in range(3)})
        row.update({f'hasArgument{n + 1}': NS['argument'] + args[n] if n < len(args) else '' for n in range(4)})
        add('specification', s, row)
    for s in set(g.subjects(RDF.type, B.Argument)):
        add('argument', s, {'label': one(s, RDFS.label), 'type': kind_of(s),
                            'argumentValue': one(s, B.hasArgumentValue), 'hasParameter': one(s, B.hasParameter),
                            'test': owner[('argument', uuid(s))]})
    for cls in (B.ActedUpon, B.Consulted):
        for s in set(g.subjects(RDF.type, cls)):
            terms = values(s, B.composedOf)
            kind_name = kind_of(s)
            agg = one(s, B.aggregatesResponsesFrom)
            definition = (f'An information element of type {kind_name}, composed of '
                          + ', '.join(curie(t) for t in terms) + '.')
            if agg:
                definition = definition[:-1] + f': the outcomes of the Responses of bdqtest:{labels[agg]} across a MultiRecord.'
            add('informationelement', s, {
                'label': one(s, RDFS.label), 'prefLabel': one(s, SKOS.prefLabel), 'type': kind_name,
                'definition': definition, 'note': one(s, SKOS.note), 'aggregatesResponsesFrom': agg,
                'composedOf': '|'.join(terms)})
    for s in set().union(*(whole.subjects(RDF.type, c) for c in POLICY_CLASSES)):
        members = sorted(str(o)[len(TNS + 'version/'):-len('-0000-00-00')] for o in whole.objects(s, B.includedInPolicy))
        add('policy', s, {'label': one(s, RDFS.label, whole), 'prefLabel': one(s, SKOS.prefLabel, whole),
                          'type': kind_of(s, whole), 'hasUseCase': one(s, B.hasUseCase, whole),
                          'members': '|'.join(TNS + m for m in members)})

    # Version links, in dependency order; an element gets a version when its row changes.
    element_rows[date] = {}
    for kind in KINDS:
        chosen = []
        for u, row in sorted(found[kind].items()):
            row = dict(row)
            if kind == 'specification':
                for n in range(1, 5):
                    a = row[f'hasArgument{n}'][len(NS['argument']):]
                    row[f'hasArgument{n}Version'] = eversion('argument', a, element_version[('argument', a)]) if a else ''
            elif kind == 'method':
                for p in FOR.values():
                    row[f'{p}Version'] = tversion(row['test'], date) if row[p] else ''
                s_ = row['hasSpecification'][len(NS['specification']):]
                row['hasSpecificationVersion'] = eversion('specification', s_, element_version[('specification', s_)])
            elif kind == 'policy':
                row['memberVersions'] = '|'.join(tversion(m[len(TNS):], test_version[m[len(TNS):]])
                                                 for m in row['members'].split('|') if m)
            if emitted.get((kind, u)) != row:
                emitted[(kind, u)] = row
                element_version[(kind, u)] = date
                chosen.append(row)
                if kind in ('argument', 'specification') and test_version[row['test']] != date:
                    problems.append(f'{date}: {kind} {u} changed without a version of its Test {row["test"]}')
        element_rows[date][kind] = chosen

    # The Test rows: owl:sameAs, the links to their information elements, and the GUID table's UUIDs.
    changed_ies = {r['term_localName'] for r in element_rows[date]['informationelement']}
    for r in rows:
        tv = rdflib.URIRef(tversion(r['term_localName'], date))
        r['sameAs'] = 'urn:uuid:' + r['term_localName']
        for prop, col in ((B.hasActedUponInformationElement, 'hasActedUponInformationElement'),
                          (B.hasConsultedInformationElement, 'hasConsultedInformationElement')):
            nodes = [uuid(o) for o in g.objects(tv, prop)]
            r[col] = NS['informationelement'] + nodes[0] if nodes else ''
            r[col + 'Version'] = (eversion('informationelement', nodes[0], element_version[('informationelement', nodes[0])])
                                  if nodes else '')
        guids = additional.get(r['term_localName'])
        if guids:
            r['methodGuid'], r['specificationGuid'] = guids['method'], guids['spec']
    for (d, r) in snapshot.values():
        for col in ('hasActedUponInformationElement', 'hasConsultedInformationElement'):
            ie = r.get(col, '')[len(NS['informationelement']):]
            if ie in changed_ies and d != date:
                problems.append(f'{date}: information element {ie} changed without a version of Test {r["term_localName"]}')

if problems:
    sys.exit('\n'.join(problems))


# Write the inputs.
class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def columns(kind):
    out = []
    for f in FIELDS[kind]:
        if f[0] not in out:
            out.append(f[0])
    return ['term_localName'] + out


TEST_HEADER = HEADER + [c for c in TEST_ADDED if c not in HEADER]
for p, date in zip(releases, dates):
    if date not in test_rows:
        continue
    for kind in KINDS:
        cols = columns(kind)
        write_csv(p / f'{PREFIX[kind]}.csv', [cols] + [[r.get(c, '') for c in cols] for r in element_rows[date][kind]])
    write_csv(p / 'bdqtest.csv', [TEST_HEADER] + [[r.get(c, '') for c in TEST_HEADER] for r in test_rows[date]])
    text = (p / 'config.yaml').read_text(encoding='utf-8')
    header = ''.join(line for line in text.splitlines(True) if line.startswith('#'))
    config = yaml.safe_load(text[len(header):])
    vocabulary = next(v for v in config['vocabularies'] if v['vocabulary'] == 'https://rs.tdwg.org/bdqtest/')
    base = next(n for n in vocabulary['namespaces'] if n['database'] == 'bdqtest')
    namespaces = [base]
    for kind in KINDS:
        namespaces.append({
            'namespace_uri': NS[kind], 'label': LABELS[kind][0], 'description': LABELS[kind][1],
            'pref_namespace_prefix': PREFIX[kind], 'database': PREFIX[kind], 'borrowed': False,
            'new_term_list': date == first, 'utility_namespace': False, 'termlist_uri': '',
            # Required by process.py; the HTML of an element is redirected by <dataset>-redirects.csv
            # (to its Test's anchor, a Policy to its Use Case, an information element to its own page).
            'prepend_url': base['prepend_url'],
            'use_namespace_in_fragment': True, 'separator': '_'})
    vocabulary['namespaces'] = namespaces
    (p / 'config.yaml').write_text(header + yaml.dump(config, Dumper=Dumper, sort_keys=False, allow_unicode=True,
                                                      width=1000), encoding='utf-8')

# Mappings, in the first bdqtest release.
templates = here.parent / 'files_for_new'
first_dir = here / f'bdq-revisions-{first}' / 'mappings'
STANDARD = {'current': read_csv(templates / 'current_terms/simple-vocabulary-column-mappings.csv')[:9],
            'versions': read_csv(templates / 'versions/simple-vocabulary-versions-column-mappings.csv')[:8]}
namespace_csv = {'current': read_csv(templates / 'current_terms/namespace.csv'),
                 'versions': read_csv(templates / 'versions/namespace.csv')}
for form in namespace_csv:
    namespace_csv[form] += [n for n in NAMESPACES if not any(r and r[0] == n[0] for r in namespace_csv[form])]


def mapping_rows(fields, form):
    index = 4 if form == 'current' else 5
    return [[c, pred, typ, '', attr, '$root'] for c, pred, typ, attr, *flags in fields
            if pred and flags[index - 4]]


for kind in KINDS:
    db = PREFIX[kind]
    current = STANDARD['current'] + mapping_rows(FIELDS[kind], 'current')
    versions = (STANDARD['versions'] + [['term_localName', 'dcterms:isVersionOf', 'iri', NS[kind], '', '$root']]
                + mapping_rows(FIELDS[kind], 'versions'))
    write_csv(first_dir / db / f'{db}-column-mappings.csv', current)
    write_csv(first_dir / db / 'namespace.csv', namespace_csv['current'])
    write_csv(first_dir / f'{db}-versions' / f'{db}-versions-column-mappings.csv', versions)
    write_csv(first_dir / f'{db}-versions' / 'namespace.csv', namespace_csv['versions'])
    # Linked tables: versions and replacements, as process.py sets them, and the many-valued links,
    # written by bdqtest_graphs.py; 'null': no back-link from the linked resource.
    linked = [['link_column', 'link_property', 'suffix1', 'link_characters', 'suffix2', 'filename', 'forward_link'],
              ['term_localName', 'dcterms:isVersionOf', 'version', 'http', '', f'{db}-versions.csv', 'dcterms:hasVersion'],
              ['replaced_term_localName', 'dcterms:replaces', 'replacing_term', 'http', '', f'{db}-replacements.csv',
               'dcterms:isReplacedBy']]
    linked_versions = [linked[0], ['replaced_version_localName', 'dcterms:replaces', 'replacing_version', 'http', '',
                                   f'{db}-versions-replacements.csv', 'dcterms:isReplacedBy']]
    many = {'policy': ('bdqffdq:includedInPolicy', 'members'),
            'informationelement': ('bdqffdq:composedOf', 'composedof')}.get(kind)
    if many:
        prop, suffix = many
        linked.append(['term_localName', 'null', 'object', 'http', '', f'{db}-{suffix}.csv', prop])
        linked_versions.append(['versionLocalName', 'null', 'object', 'http', '', f'{db}-versions-{suffix}.csv', prop])
        for folder, name in ((db, f'{db}-{suffix}'), (f'{db}-versions', f'{db}-versions-{suffix}')):
            write_csv(first_dir / folder / f'{name}-column-mappings.csv', [['header', 'predicate', 'type', 'value', 'attribute', 'subject_id']])
            write_csv(first_dir / folder / f'{name}-classes.csv', [['id', 'class'], ['$root', 'null']])
    write_csv(first_dir / db / 'linked-classes.csv', linked)
    write_csv(first_dir / f'{db}-versions' / 'linked-classes.csv', linked_versions)

# bdqtest: the added mappings, after the existing ones.
for form, path in (('current', first_dir / 'bdqtest' / 'bdqtest-column-mappings.csv'),
                   ('versions', first_dir / 'bdqtest-versions' / 'bdqtest-versions-column-mappings.csv')):
    rows = [r for r in read_csv(path) if r[0] not in TEST_ADDED]
    write_csv(path, rows + mapping_rows(TEST_FIELDS, form))
    ns_path = path.parent / 'namespace.csv'
    ns = read_csv(ns_path)
    write_csv(ns_path, ns + [n for n in NAMESPACES if not any(r and r[0] == n[0] for r in ns)])

counts = {k: (len({u for (kk, u) in element_version if kk == k}),
              sum(len(element_rows[d][k]) for d in element_rows)) for k in KINDS}
print('bdqtest elements (elements, versions): ' + ', '.join(f'{k} {c[0]}, {c[1]}' for k, c in counts.items()))
