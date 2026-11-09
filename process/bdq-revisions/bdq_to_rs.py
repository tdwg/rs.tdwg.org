"""Convert the five simple BDQ vocabularies to rs.tdwg.org release inputs.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340). This is a one-way bootstrap from
the files in tdwg/bdq, used to create the inputs for the public review at
bdq-public-review.rs.tdwg.org. It is not part of the rs.tdwg.org processing
workflow and is intended to be replaced: once BDQ's vocabulary metadata live
authoritatively in this repository (the release-input CSVs, config.yaml and
mapping files under process/bdq-revisions/), those files are edited directly
and this script is no longer run. Don't run it over inputs that have since
been edited by hand, since it rewrites them.

Reads   <bdq>/tg2/_review/vocabulary/bdq{dim,enh,crit,uc,val}_term_versions.csv
        <bdq>/tg2/_build_review/templates/list/<vocab>/document_configuration.yaml
        <bdq>/tg2/_build_review/templates/standard_landing/document_configuration.yaml
        <bdq>/tg2/_build_review/authors_configuration.yaml
        <rs>/process/files_for_new/{current_terms,versions}/simple-cv*-column-mappings.csv
Writes  <rs>/process/bdq-revisions/bdq-revisions-<date_issued>/
            <prefix>.csv              release-input CSVs
            mappings/<db>/...         BDQ column mappings and namespace.csv
            config.yaml               the release declaration

The mapping follows the RDF that tg2/_build_review/draft_build-termlist.py writes
(tg2/_review/dist/bdq*.xml); see the plan, tdwg/bdq
tg2/_make_review/deployment_rs_tdwg_org.md, Section 8.3. The inputs in
bdq-revisions-2026-11-09/ were generated from tdwg/bdq master 10a5d682.

Requires pyyaml. Usage: python -I bdq_to_rs.py <bdq_repo> <rs_repo> <date_issued>
"""
import csv, io, sys, pathlib, xml.dom.minidom
import yaml

bdq, rs, date_issued = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
release_dir_rel = f'bdq-revisions/bdq-revisions-{date_issued}'
release_dir = rs / 'process' / release_dir_rel
VOCABS = ['bdqdim', 'bdqenh', 'bdqcrit', 'bdquc', 'bdqval']
CURIES = {
    'bdqffdq': 'https://rs.tdwg.org/bdqffdq/terms/',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
}
XHTML_DIV = '<div xmlns="http://www.w3.org/1999/xhtml">{}</div>'

# Release-input columns, identical for all five vocabularies (unused cells are empty).
HEADER = ['term_localName', 'label', 'prefLabel', 'definition', 'usage', 'notes',
          'controlled_value_string', 'skos_inScheme', 'type', 'type1', 'hasFitnessRequirements']

# PROVISIONAL for the review: prepend_url and browserRedirectUri (current /draft/
# locations), and these vocabulary / term list labels and descriptions (drafted here,
# to be reviewed by BDQ). Document IRIs were decided 2026-11-09 (plan Section 11.3).
VOCAB_TEXT = {
    'bdqdim': ('Data Quality Dimension Controlled Vocabulary', 'Data Quality Dimension', 'bdqffdq:DataQualityDimension', 'bdqffdq:hasDataQualityDimension'),
    'bdqenh': ('Data Quality Enhancement Controlled Vocabulary', 'Data Quality Enhancement', 'bdqffdq:Enhancement', 'bdqffdq:hasEnhancement'),
    'bdqcrit': ('Data Quality Criterion Controlled Vocabulary', 'Data Quality Criterion', 'bdqffdq:Criterion', 'bdqffdq:hasCriterion'),
    'bdquc': ('BDQ Use Case Controlled Vocabulary', 'BDQ Use Case', 'bdqffdq:UseCase', None),
    'bdqval': ('BDQ Controlled Vocabulary', 'BDQ', None, None),
}
CREATOR = 'TDWG Biodiversity Data Quality Interest Group Task Group 2: Data Quality Tests and Assertions'

def expand(curie):
    curie = curie.strip()
    if curie.startswith(('http://', 'https://')):
        return curie
    prefix, _, local = curie.partition(':')
    return CURIES[prefix] + local

def xml_literal(text, where):
    if not text.strip():
        return ''
    value = XHTML_DIV.format(text)   # source text kept exactly, as in BDQ's RDF
    try:
        xml.dom.minidom.parseString(value)
    except Exception as e:
        raise SystemExit(f'{where}: not well-formed XML ({e}): {text[:120]!r}')
    return value

def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))

report = []
for v in VOCABS:
    ns = f'https://rs.tdwg.org/{v}/terms/'
    src = list(csv.DictReader(open(bdq / f'tg2/_review/vocabulary/{v}_term_versions.csv', newline='', encoding='utf-8')))
    out = [HEADER]
    for r in src:
        name = r['term_localName']
        types = [expand(t) for t in r['rdf_type'].split(',') if t.strip()]
        if len(types) > 2:
            raise SystemExit(f'{v}:{name}: more than two rdf:type values')
        if r['controlled_value_string'] != name:
            report.append(f'{v}:{name}: rdf:value from term_localName {name!r}; '
                          f'controlled_value_string column was {r["controlled_value_string"]!r}')
        out.append([
            name, r['label'].rstrip(), r['prefLabel'].rstrip(), r['definition'].rstrip(),
            (r.get('scopeNote') or '').rstrip(),
            xml_literal(r['comments'], f'{v}:{name}:comments'),
            name,                    # rdf:value, as in BDQ's RDF (term_localName)
            ns,                      # skos:inScheme the term list IRI, as in BDQ's RDF
            types[0], types[1] if len(types) > 1 else '',
            xml_literal(r.get('hasFitnessRequirements', ''), f'{v}:{name}:hasFitnessRequirements'),
        ])
    write_csv(release_dir / f'{v}.csv', out)
    report.append(f'{v}: {len(src)} terms -> {release_dir_rel}/{v}.csv')

    # Column mappings: the simple controlled vocabulary (vocab_type 2) templates, edited.
    for kind, template, target in (
        ('current_terms', 'simple-cv-column-mappings.csv', f'{v}-column-mappings.csv'),
        ('versions', 'simple-cv-versions-column-mappings.csv', f'{v}-versions-column-mappings.csv'),
    ):
        rows = read_csv(rs / 'process/files_for_new' / kind / template)
        head, body = rows[0], rows[1:]
        edited = []
        for row in body:
            h, pred = row[0], row[1]
            if h == 'label' and pred == 'skos:prefLabel':
                row = ['prefLabel', 'skos:prefLabel', 'language', '', 'en', '$root']
            elif h == 'usage':
                row = ['usage', 'skos:scopeNote', 'datatype', '', 'xsd:string', '$root']
            elif h == 'notes':
                row = ['notes', 'skos:note', 'datatype', '', 'rdf:XMLLiteral', '$root']
            elif h == 'skos_inScheme':
                row = ['skos_inScheme', 'skos:inScheme', 'iri', '', '', '$root']   # cell holds the full IRI
            elif h == 'term_localName':                                        # versions: dcterms:isVersionOf
                row = row[:3] + [ns] + row[4:]
            edited.append(row)
            if h == 'type':
                edited.append(['type1', 'rdf:type', 'iri', '', '', '$root'])
        edited.append(['hasFitnessRequirements', 'bdqffdq:hasFitnessRequirements', 'datatype', '', 'rdf:XMLLiteral', '$root'])
        dest = 'mappings/' + (v if kind == 'current_terms' else v + '-versions') + '/' + target
        write_csv(release_dir / dest, [head] + edited)
    for d in (v, v + '-versions'):
        base = 'current_terms' if d == v else 'versions'
        nsrows = read_csv(rs / 'process/files_for_new' / base / 'namespace.csv')
        if not any(r and r[0] == 'bdqffdq' for r in nsrows):
            nsrows.append(['bdqffdq', CURIES['bdqffdq']])
        write_csv(release_dir / f'mappings/{d}/namespace.csv', nsrows)

# Contributors: BDQ's shared authors_configuration.yaml.
contributors = yaml.safe_load(open(bdq / 'tg2/_build_review/authors_configuration.yaml', encoding='utf-8'))
for c in contributors:
    for k in ('contributor_iri', 'contributor_literal', 'contributor_role', 'role_uri', 'affiliation', 'affiliation_uri'):
        c[k] = '' if c.get(k) is None else c[k]

vocabularies, documents = [], []
for v in VOCABS:
    label, short, cls, prop = VOCAB_TEXT[v]
    doc = yaml.safe_load(open(bdq / f'tg2/_build_review/templates/list/{v}/document_configuration.yaml', encoding='utf-8'))
    doc_iri = f'https://rs.tdwg.org/{v}/doc/list/'                         # decided 2026-11-09
    desc = (f'A controlled vocabulary of the {cls} individuals defined by the BDQ standard'
            + (f', used as values of {prop}.' if prop else '.')) if cls else \
           'A vocabulary of terms used in BDQ Test Specifications, especially values used as bdqffdq:Parameters.'
    vocabularies.append({
        'vocabulary': f'https://rs.tdwg.org/{v}/',
        'vocab_type': 2,
        'list_of_terms_iri': doc_iri,
        'vocabulary_label': label,
        'vocabulary_description': desc,
        'dc_creator': CREATOR,
        'dcterms_license': 'https://creativecommons.org/licenses/by/4.0/',
        'namespaces': [{
            'namespace_uri': f'https://rs.tdwg.org/{v}/terms/',
            'label': f'{short} controlled values list',
            'description': f'Controlled values list for the {label}',
            'pref_namespace_prefix': v,
            'database': v,
            'borrowed': False,
            'new_term_list': True,
            'utility_namespace': False,
            'termlist_uri': '',
            'prepend_url': f'https://bdq.tdwg.org/draft/docs/list/{v}/#',          # PROVISIONAL
            'use_namespace_in_fragment': True,
            'separator': '_',
        }],
    })
    documents.append({
        'document': doc_iri,
        'documentTitle': doc['documentTitle'],
        'abstract': doc['abstract'],
        'creator': doc['creator'],
        'mediaType': doc['mediaType'],
        'accessUrl': doc['accessUrl'],
        'browserRedirectUri': f'https://bdq.tdwg.org/draft/docs/list/{v}/',      # PROVISIONAL
        'contributors': contributors,
    })

landing = yaml.safe_load(open(bdq / 'tg2/_build_review/templates/standard_landing/document_configuration.yaml', encoding='utf-8'))
config = {
    'standard_label': 'Biodiversity Data Quality (BDQ)',
    'standard': 'http://www.tdwg.org/standards/YYY',
    'standard_description': landing['abstract'].split('<br>', 1)[1].strip(),
    'standard_status': 'Draft Standard',
    'date_issued': date_issued,
    'local_offset_from_utc': '-05:00',
    'decision_number': 'YYY',
    'decisions_text': 'BDQ terms published for public review; not ratified.',
    'revision_directory': 'bdq-revisions',
    'release_directory': release_dir_rel,
    'document_defaults': {
        'publisher': 'Biodiversity Information Standards (TDWG)',
        'license_statement': 'Licensed under a Creative Commons Attribution 4.0 International (CC BY) License.',
        'license_uri': 'https://creativecommons.org/licenses/by/4.0/',
        'comment': 'Draft Standard for Review',
    },
    'documents': documents,
    'vocabularies': vocabularies,
}
class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data): return True
text = ('# BDQ release declaration for bdq-public-review.rs.tdwg.org (tdwg/bdq#340).\n'
        '# Generated from tdwg/bdq tg2/_review/vocabulary/*_term_versions.csv and the List of Terms\n'
        '# document_configuration.yaml files (plan Section 8.3). Run with:\n'
        '#   python process.py --config bdq-revisions/bdq-revisions-' + date_issued + '/config.yaml\n'
        '# Placeholders for the public review: standard YYY, decision_number YYY (plan 8.2.1).\n'
        '# Provisional: prepend_url and browserRedirectUri (/draft/ locations, plan 8.6), and the\n'
        '# vocabulary and term list labels and descriptions (drafted, to be reviewed by BDQ).\n'
        '# After the first run, set new_term_list: false for reruns (plan 8.3, Rerunning).\n'
        + yaml.dump(config, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000))
(release_dir / 'config.yaml').write_text(text, encoding='utf-8')
print('\n'.join(report))
