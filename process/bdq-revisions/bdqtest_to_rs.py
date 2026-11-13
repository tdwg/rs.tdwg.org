"""Convert the BDQ Tests (bdqtest) to rs.tdwg.org release inputs.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340), like bdq_to_rs.py and
bdqffdq_to_rs.py: a one-way bootstrap from the files in tdwg/bdq, intended to be
replaced by the authoritative inputs kept in this repository. Once the bdqtest
rows, mapping files and release declarations under process/bdq-revisions/ are
edited directly, this script is no longer run. Don't run it over inputs that
have since been edited by hand, since it rewrites them.

Plan (tdwg/bdq tg2/_make_review/deployment_rs_tdwg_org.md), Sections 10 and 10.9:
- bdqtest is a flat term list with versions (option T3); the full graph of each
  Test version (Method, Specification, Arguments, information elements,
  Policies) is generated separately and appended to its RDF by rs.tdwg.org.
- Each Test gets two versions on bdq-public-review.rs.tdwg.org (10.9.3): one on
  its DateLastUpdated (the behavioral version that implementations cite) and one
  on its issued date (the latest); one only where the two dates are equal. Both
  carry the Test's current content (placeholders), except for the four
  single-record Measures that count Test outcomes (10.9.7), whose versions
  before their remodeling on 2026-11-12 carry their content from before tdwg/bdq
  ac825581.
- All columns of bdqtest_term_versions.csv are carried, renamed to legal XML
  names (COLUMNS below, the mapping back to the published names; Section 10.8).
  Columns derived here hold the IRIs that BDQ's RDF puts on the Test node
  (tg2/_build_review/build_bdqtest_rdf.py, as in kurator-ffdq). The term-level
  RDF mirrors the Test node; the prefLabel composed as "<prefLabel> for
  <Resource Type>" is made by the graph generator, as now.

Reads   <bdq>/tg2/_review/vocabulary/bdqtest_term_versions.csv (current)
        <old_csv>: the same file at tdwg/bdq ac825581^ (before the remodeling)
        <bdq>/tg2/_build_review/templates/list/bdqtest/document_configuration.yaml
        <rs>/process/files_for_new/{current_terms,versions}/simple-vocabulary*-column-mappings.csv
Writes  <rs>/process/bdq-revisions/bdq-revisions-<date>/
            bdqtest.csv                     release-input rows of that date
            config.yaml                     bdqtest declared from its first release on
            mappings/bdqtest{,-versions}/   in the first bdqtest release
            bdqtest-graph-inputs/           the GUID tables of tdwg/bdq tg2/core/, where they change
        and creates the release directories for new dates, declared as the
        release before them (or, before the first existing release, with bdqtest
        alone).

Requires pyyaml. Usage: python -I bdqtest_to_rs.py <bdq_repo> <rs_repo> <old_csv>
"""
import copy, csv, pathlib, sys
import yaml

bdq, rs, old_csv = (pathlib.Path(a) for a in sys.argv[1:4])
revisions = rs / 'process' / 'bdq-revisions'
NS = 'https://rs.tdwg.org/bdqtest/terms/'
REMODELED = {'MEASURE_VALIDATIONTESTS_COMPLIANT', 'MEASURE_VALIDATIONTESTS_NOTCOMPLIANT',
             'MEASURE_VALIDATIONTESTS_PREREQUISITESNOTMET', 'MEASURE_AMENDMENTS_PROPOSED'}
REMODELED_DATE = '2026-11-12'

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))   # also when run with python -I
from bdqtest_columns import COLUMNS, DERIVED, HEADER   # noqa: E402


# Term-level RDF, mirroring the Test node; the other columns are carried, not emitted.
MAPPINGS = [
    ['label', 'rdfs:label', 'language', '', 'en', '$root'],
    ['definition', 'rdfs:comment', 'language', '', 'en', '$root'],
    ['definition', 'skos:definition', 'language', '', 'en', '$root'],
    ['description', 'dcterms:description', 'language', '', 'en', '$root'],
    ['notes', 'skos:note', 'language', '', 'en', '$root'],
    ['historyNoteUrl', 'skos:historyNote', 'datatype', '', 'xsd:string', '$root'],
    ['dateLastUpdated', 'bdqffdq:hasDateLastUpdated', 'datatype', '', 'xsd:date', '$root'],
    ['type', 'rdf:type', 'iri', '', '', '$root'],
    ['hasResourceType', 'bdqffdq:hasResourceType', 'iri', '', '', '$root'],
    ['hasDataQualityDimension', 'bdqffdq:hasDataQualityDimension', 'iri', '', '', '$root'],
    ['hasCriterion', 'bdqffdq:hasCriterion', 'iri', '', '', '$root'],
    ['hasEnhancement', 'bdqffdq:hasEnhancement', 'iri', '', '', '$root'],
]
PREFIXES = [
    ['bdqffdq', 'https://rs.tdwg.org/bdqffdq/terms/'],
    ['bdqdim', 'https://rs.tdwg.org/bdqdim/terms/'],
    ['bdqcrit', 'https://rs.tdwg.org/bdqcrit/terms/'],
    ['bdqenh', 'https://rs.tdwg.org/bdqenh/terms/'],
    ['bdqtest', NS],
]

# PROVISIONAL for the review, like the other BDQ vocabularies' labels and descriptions.
VOCABULARY = {
    'vocabulary': 'https://rs.tdwg.org/bdqtest/',
    'vocab_type': 1,
    'list_of_terms_iri': 'https://rs.tdwg.org/bdqtest/doc/list/',
    'vocabulary_label': 'BDQ Tests Vocabulary',
    'vocabulary_description': 'The BDQ Tests: each a bdqffdq:Validation, bdqffdq:Issue, bdqffdq:Measure, or '
                              'bdqffdq:Amendment, with its Method, Specification, Arguments, information elements, '
                              'and the Policies that include it.',
    'dc_creator': 'TDWG Biodiversity Data Quality Interest Group Task Group 2: Data Quality Tests and Assertions',
    'dcterms_license': 'https://creativecommons.org/licenses/by/4.0/',
    'namespaces': [{
        'namespace_uri': NS,
        'label': 'Data Quality Test terms',
        'description': 'Term list for the BDQ Tests vocabulary.',
        'pref_namespace_prefix': 'bdqtest',
        'database': 'bdqtest',
        'borrowed': False,
        'new_term_list': False,
        'utility_namespace': False,
        'termlist_uri': '',
        'prepend_url': 'https://bdq.tdwg.org/draft/docs/list/bdqtest/#',   # PROVISIONAL (/draft/)
        'use_namespace_in_fragment': True,
        'separator': '_',
    }],
}


def read_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)


def convert(row):
    """One bdqtest_term_versions.csv row as a release-input row."""
    out = {rs_name: row[name].strip() for name, rs_name in COLUMNS.items() if rs_name}
    test_type = row['Type'].strip()
    out['type'] = 'bdqffdq:' + test_type
    out['hasResourceType'] = 'bdqffdq:' + row['Resource Type'].strip() if row['Resource Type'].strip() else ''
    out['hasDataQualityDimension'] = 'bdqdim:' + row['Dimension'].strip() if row['Dimension'].strip() else ''
    # As build_bdqtest_rdf.py: a Criterion for Validations and Issues, an Enhancement for Amendments.
    out['hasCriterion'] = ('bdqcrit:' + row['Criterion'].strip()
                           if row['Criterion'].strip() and test_type in ('Validation', 'Issue') else '')
    out['hasEnhancement'] = ('bdqenh:' + row['Enhancement'].strip()
                             if row['Enhancement'].strip() and test_type == 'Amendment' else '')
    return [out[c] for c in HEADER]


current = read_rows(bdq / 'tg2/_review/vocabulary/bdqtest_term_versions.csv')
old = {r['Label']: r for r in read_rows(old_csv)}
missing = set(COLUMNS) - set(current[0])
if missing:
    sys.exit('columns missing from bdqtest_term_versions.csv: ' + ', '.join(sorted(missing)))
unknown = set(current[0]) - set(COLUMNS)
if unknown:
    sys.exit('columns not in the mapping: ' + ', '.join(sorted(unknown)))

# The versions of each Test, by date.
by_date = {}
for row in current:
    label, dlu, issued = row['Label'].strip(), row['DateLastUpdated'].strip(), row['issued'].strip()
    if dlu > issued:
        sys.exit(f'{label}: DateLastUpdated {dlu} is later than issued {issued}')
    if label in REMODELED:
        before = old[label]
        if not (dlu == issued == REMODELED_DATE):
            sys.exit(f'{label}: expected DateLastUpdated and issued {REMODELED_DATE}')
        for date in sorted({before['DateLastUpdated'].strip(), before['issued'].strip()}):
            by_date.setdefault(date, []).append(convert(before))
        by_date.setdefault(REMODELED_DATE, []).append(convert(row))
    else:
        for date in sorted({dlu, issued}):
            by_date.setdefault(date, []).append(convert(row))
dates = sorted(by_date)
first = dates[0]

# The release directories: existing ones, plus one for each new date.
existing = sorted(p.name[len('bdq-revisions-'):] for p in revisions.glob('bdq-revisions-20*') if p.is_dir())


class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def load_config(date):
    text = (revisions / f'bdq-revisions-{date}' / 'config.yaml').read_text(encoding='utf-8')
    header = ''.join(l for l in text.splitlines(True) if l.startswith('#'))
    return header, yaml.safe_load(text[len(header):])


def save_config(date, header, config):
    (revisions / f'bdq-revisions-{date}' / 'config.yaml').write_text(
        header + yaml.dump(config, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')


doc_source = yaml.safe_load(open(bdq / 'tg2/_build_review/templates/list/bdqtest/document_configuration.yaml', encoding='utf-8'))
_, template = load_config(existing[0])
contributors = next(d['contributors'] for d in template['documents'])   # BDQ's shared author list
DOCUMENT = {
    'document': VOCABULARY['list_of_terms_iri'],
    'documentTitle': doc_source['documentTitle'],
    'abstract': doc_source['abstract'],
    'creator': doc_source['creator'],
    'mediaType': doc_source['mediaType'],
    'accessUrl': 'https://raw.githubusercontent.com/tdwg/bdq/master/tg2/_review/docs/list/bdqtest/index.md',
    'browserRedirectUri': 'https://bdq.tdwg.org/draft/docs/list/bdqtest/',   # PROVISIONAL (/draft/)
    'contributors': contributors,
}

for date in dates:
    if date in existing:
        continue
    earlier = sorted(d for d in existing if d < date)
    d = revisions / f'bdq-revisions-{date}'
    d.mkdir()
    if earlier:
        base_header, config = load_config(earlier[-1])
        for vocabulary in config['vocabularies']:
            for namespace in vocabulary['namespaces']:
                namespace['new_term_list'] = False
    else:   # before the first existing release: bdqtest alone
        base_header, config = load_config(existing[0])
        config['vocabularies'] = []
        config['documents'] = []
    config['date_issued'] = date
    config['release_directory'] = f'bdq-revisions/bdq-revisions-{date}'
    header = (f'# BDQ draft release {date} for bdq-public-review.rs.tdwg.org (tdwg/bdq#340).\n'
              '# Placeholder bdqtest versions dated from the BDQ draft (DateLastUpdated and issued;\n'
              '# plan Sections 8.5, 10.9.3). Created by bdqtest_to_rs.py from the release before it.\n'
              f'# Run with: python process.py --config bdq-revisions/bdq-revisions-{date}/config.yaml\n'
              + ''.join(l for l in base_header.splitlines(True)[4:]))
    for vocabulary in config['vocabularies']:
        prefix = vocabulary['namespaces'][0]['pref_namespace_prefix']
        with open(revisions / f'bdq-revisions-{earlier[-1]}' / f'{prefix}.csv', newline='', encoding='utf-8') as f:
            write_csv(d / f'{prefix}.csv', [next(csv.reader(f))])   # header only
    save_config(date, header, config)
    existing.append(date)
existing.sort()

# Declare bdqtest in every release from its first one on, and write its rows.
for date in existing:
    if date < first:
        continue
    header, config = load_config(date)
    config['vocabularies'] = [v for v in config['vocabularies'] if v['vocabulary'] != VOCABULARY['vocabulary']]
    vocabulary = copy.deepcopy(VOCABULARY)
    vocabulary['namespaces'][0]['new_term_list'] = (date == first)
    config['vocabularies'].append(vocabulary)
    config['documents'] = [x for x in config['documents'] if x['document'] != DOCUMENT['document']] + [copy.deepcopy(DOCUMENT)]
    save_config(date, header, config)
    write_csv(revisions / f'bdq-revisions-{date}' / 'bdqtest.csv', [HEADER] + by_date.get(date, []))

# Column mappings, in the first bdqtest release: the simple vocabulary templates, edited.
def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))


DROPPED = {'label', 'definition', 'usage', 'notes', 'examples', 'type', 'tdwgutility_organizedInClass'}
for kind, template_file, target, dest in (
    ('current_terms', 'simple-vocabulary-column-mappings.csv', 'bdqtest-column-mappings.csv', 'bdqtest'),
    ('versions', 'simple-vocabulary-versions-column-mappings.csv', 'bdqtest-versions-column-mappings.csv', 'bdqtest-versions'),
):
    rows = read_csv(rs / 'process/files_for_new' / kind / template_file)
    out = [rows[0]]
    for row in rows[1:]:
        if row[0] in DROPPED:
            continue
        if row[0] == 'term_localName':        # versions: dcterms:isVersionOf
            row = row[:3] + [NS] + row[4:]
        out.append(row)
    out.extend(MAPPINGS)
    write_csv(revisions / f'bdq-revisions-{first}' / 'mappings' / dest / target, out)
    namespace = read_csv(rs / 'process/files_for_new' / kind / 'namespace.csv')
    namespace += [p for p in PREFIXES if not any(r and r[0] == p[0] for r in namespace)]
    write_csv(revisions / f'bdq-revisions-{first}' / 'mappings' / dest / 'namespace.csv', namespace)

# The generator's GUID tables (tdwg/bdq tg2/core/), in the releases where they change: as they were
# before the remodeling (ac825581^) from the first bdqtest release on, and the current
# information element table from the remodeling on (bdqtest_graphs.py uses the latest copy on or
# before each version's date).
import subprocess   # noqa: E402
GRAPH_INPUTS = ['TG2_tests_additional_guids.csv', 'information_element_guids.csv',
                'TG2_policy_guids.csv', 'TG2_citation_guids.csv']
for name in GRAPH_INPUTS:
    data = subprocess.run(['git', '-C', str(bdq), 'show', f'ac825581^:tg2/core/{name}'],
                          check=True, capture_output=True).stdout
    target = revisions / f'bdq-revisions-{first}' / 'bdqtest-graph-inputs' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
for name in GRAPH_INPUTS:
    now = (bdq / 'tg2/core' / name).read_bytes()
    if now != (revisions / f'bdq-revisions-{first}' / 'bdqtest-graph-inputs' / name).read_bytes():
        target = revisions / f'bdq-revisions-{REMODELED_DATE}' / 'bdqtest-graph-inputs' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(now)

print(f'bdqtest: {len(current)} Tests, {sum(len(v) for v in by_date.values())} versions on {len(dates)} dates '
      f'({first} to {dates[-1]}); first release {first}')
