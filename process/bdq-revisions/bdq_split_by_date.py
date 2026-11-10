"""Split the BDQ release inputs into draft releases, one per draft date.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340), like bdq_to_rs.py and
bdqffdq_to_rs.py, and intended to be replaced by the authoritative inputs kept
in this repository.

Plan Section 8.5 (decided 2026-11-09): on bdq-public-review.rs.tdwg.org, each
BDQ term gets a placeholder term version dated when its current content last
changed in the BDQ draft (issued in tdwg/bdq tg2/_review/vocabulary/
*_term_versions.csv; dcterms:issued in bdqffdq.owl). On ratification these
become real term versions with the release date. The release is replayed as a
sequence of draft releases, one per date, each adding the terms whose content
dates from it, followed by the 2026-11-09 release with the decided bdqffdq
changes (plan Section 9.5).

Input: the release directory bdq-revisions-2026-11-09 as converted (all terms,
decided bdqffdq changes applied), and the faithful bdqffdq inputs from the
conversion commit (term list, axioms, mappings before the decided changes).
Output: bdq-revisions-<date>/ for each draft date, and bdq-revisions-2026-11-09/
reduced to the rows that the decided changes alter.

Usage: python -I bdq_split_by_date.py <bdq_repo> <rs_repo> <faithful_dir> <bdqffdq_owl>
  faithful_dir: a copy of bdq-revisions-2026-11-09 at the conversion commit
  (git archive e229ed37 process/bdq-revisions/bdq-revisions-2026-11-09).
  bdqffdq_owl: the BDQ draft bdqffdq.owl with per-term dcterms:issued, i.e. tdwg/bdq
  tg2/_review/vocabulary/bdqffdq.owl before it was replaced by the generated ontology
  (git show 4aff59f0:tg2/_review/vocabulary/bdqffdq.owl).
"""
import copy, csv, pathlib, shutil, sys
import rdflib
import yaml
from rdflib.namespace import DCTERMS

bdq, rs, faithful, owl_path = (pathlib.Path(a) for a in sys.argv[1:5])
revisions = rs / 'process' / 'bdq-revisions'
final_date = '2026-11-09'
final = revisions / f'bdq-revisions-{final_date}'
SIMPLE = ['bdqdim', 'bdqenh', 'bdqcrit', 'bdquc', 'bdqval']
FFDQ = 'bdqffdq'
# Terms with no date in the BDQ source, and the date used (plan Section 8.5).
INFERRED = {('bdqffdq', 'aggregatesResponsesFrom'): '2026-04-23'}   # added in tdwg/bdq fe55c9ff with bdqval:AggregatedTestResponseOutcomes


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, lineterminator='\n').writerows([header] + rows)


# Draft date of every term.
dates = {}
for v in SIMPLE:
    with open(bdq / f'tg2/_review/vocabulary/{v}_term_versions.csv', newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            dates[(v, r['term_localName'])] = r['issued']
owl = rdflib.Graph().parse(owl_path, format='turtle')
B = 'https://rs.tdwg.org/bdqffdq/terms/'
ffdq_header, ffdq_faithful = read_csv(faithful / 'bdqffdq.csv')
for row in ffdq_faithful:
    issued = owl.value(rdflib.URIRef(B + row[0]), DCTERMS.issued)
    if issued is not None:
        dates[(FFDQ, row[0])] = str(issued)
dates.update(INFERRED)

# Rows of each vocabulary, by date (faithful content for bdqffdq).
inputs = {v: read_csv(final / f'{v}.csv') for v in SIMPLE}
inputs[FFDQ] = (ffdq_header, ffdq_faithful)
by_date = {}
for v, (header, rows) in inputs.items():
    for row in rows:
        key = (v, row[0])
        if key not in dates:
            sys.exit(f'no draft date for {v}:{row[0]}')
        by_date.setdefault(dates[key], {}).setdefault(v, []).append(row)
draft_dates = sorted(by_date)
# The faithful axioms belong to the first draft release by which every term they refer to exists.
faithful_axioms = rdflib.Graph().parse(faithful / 'bdqffdq-axioms.ttl', format='turtle')
axiom_terms = {str(n)[len(B):] for t in faithful_axioms for n in t
               if isinstance(n, rdflib.URIRef) and str(n).startswith(B) and str(n) != B}
missing = sorted(t for t in axiom_terms if (FFDQ, t) not in dates)
if missing:
    sys.exit('axioms refer to terms with no draft date: ' + ', '.join(missing))
axioms_date = max(dates[(FFDQ, t)] for t in axiom_terms)
if draft_dates[-1] >= final_date:
    sys.exit('a draft date is not before the final release')
first_date = {v: min(d for d in draft_dates if v in by_date[d]) for v in inputs}

# The final release: only the bdqffdq rows that the decided changes alter.
decided_header, decided_rows = read_csv(final / 'bdqffdq.csv')
decided = {r[0]: dict(zip(decided_header, r)) for r in decided_rows}
changed = []
for row in ffdq_faithful:
    old = dict(zip(ffdq_header, row))
    new = {h: decided[row[0]].get(h, '') for h in ffdq_header}   # columns dropped by the decision become empty
    if new != old:
        changed.append([new[h] for h in ffdq_header])

config_text = (final / 'config.yaml').read_text(encoding='utf-8')
config_header = ''.join(l for l in config_text.splitlines(True) if l.startswith('#'))
config = yaml.safe_load(config_text[len(config_header):])


class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def write_config(directory, date, vocabularies_present):
    c = copy.deepcopy(config)
    c['date_issued'] = date
    c['release_directory'] = f'bdq-revisions/bdq-revisions-{date}'
    c['vocabularies'] = [v for v in c['vocabularies'] if v['namespaces'][0]['database'] in vocabularies_present]
    for v in c['vocabularies']:
        v['namespaces'][0]['new_term_list'] = (first_date[v['namespaces'][0]['database']] == date)
    for v in c['vocabularies']:                     # the extension term list exists from axioms_date on
        if 'extension_lists' in v and date < axioms_date:
            del v['extension_lists']
    lists = {v['list_of_terms_iri'] for v in c['vocabularies']}
    c['documents'] = [d for d in c['documents'] if d['document'] in lists]
    header = (f'# BDQ draft release {date} for bdq-public-review.rs.tdwg.org (tdwg/bdq#340).\n'
              '# Placeholder term versions dated from the BDQ draft; on ratification they become\n'
              '# real term versions with the release date (plan Section 8.5).\n'
              f'# Run with: python process.py --config bdq-revisions/bdq-revisions-{date}/config.yaml\n'
              + ''.join(l for l in config_header.splitlines(True)[4:] if 'After the first run' not in l))
    (directory / 'config.yaml').write_text(header + yaml.dump(c, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')


present = set()
for date in draft_dates:
    d = revisions / f'bdq-revisions-{date}'
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for v, rows in sorted(by_date[date].items()):
        header = inputs[v][0]
        write_csv(d / f'{v}.csv', header, rows)
        if first_date[v] == date:        # the release that creates the term list carries its mappings
            for ds in (v, v + '-versions'):
                src = (faithful if v == FFDQ else final) / 'mappings' / ds
                shutil.copytree(src, d / 'mappings' / ds)
    if date == axioms_date:
        shutil.copy(faithful / 'bdqffdq-axioms.ttl', d / 'bdqffdq-axioms.ttl')
    present |= set(by_date[date])
    for v in sorted(present - set(by_date[date])):    # every declared vocabulary needs a release-input CSV
        write_csv(d / f'{v}.csv', inputs[v][0], [])
    write_config(d, date, present)
    print(date, {v: len(r) for v, r in sorted(by_date[date].items())})

# Reduce the final release to the changed bdqffdq rows; keep its decided mappings and axioms.
for v in SIMPLE:
    (final / f'{v}.csv').unlink()
    for ds in (v, v + '-versions'):
        shutil.rmtree(final / 'mappings' / ds)
write_csv(final / 'bdqffdq.csv', ffdq_header, changed)
for v in SIMPLE:
    write_csv(final / f'{v}.csv', inputs[v][0], [])
write_config(final, final_date, present)
print(final_date, {FFDQ: len(changed)}, sorted(r[0] for r in changed))
