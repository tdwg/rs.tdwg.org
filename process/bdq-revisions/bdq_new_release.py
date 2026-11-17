"""Create a BDQ release directory from proposed changes to Tests (the migration step).

FOR THE BDQ PUBLIC REVIEW (tdwg/bdq#340); plan (tdwg/bdq tg2/_make_review/deployment_rs_tdwg_org.md)
Section 13.1, flow 3, "Migration on acceptance". It automates steps 1, 2, and 5 of "Changing a
Test" in README.md: it writes bdq-revisions/bdq-revisions-<date>/ with

    config.yaml       the latest release's, with date_issued and release_directory set to <date>,
                      and modified: true on the documents given with --modified-document
                      (and on no others)
    bdqtest.csv       one row per proposed Test: its row in the latest release that has it, with
                      the proposed values
    <other>.csv       a header-only CSV for every other namespace of the latest release

The proposals are a CSV in the published BDQ column names (tdwg/bdq
tg2/_review/vocabulary/bdqtest_term_versions.csv, bdq_issue_to_csv), one row per Test, keyed on
term_localName (the Test's UUID). Only the columns present are changed; iri, term_iri, and issued
are derived by rs.tdwg.org and are ignored. A row whose UUID is in no release is a new Test and must
give every input column.

DateLastUpdated: a change is substantive if it changes the behavior implementations must follow
(plan Section 10.9.3). Give such Tests with --substantive <uuid> (or DateLastUpdated equal to the
release date in the proposal), and their dateLastUpdated becomes the release date; other changes
keep the Test's dateLastUpdated. A new Test's dateLastUpdated is the release date.

A Test row with no change is refused, unless --unchanged-test is given: for a release whose change
is in the Test's elements as the pinned builder derives them (for example the wording of Method
labels, bdqtest_rdf.py), each such Test gets a new version with the same row, and
bdqtest_elements_to_rs.py derives the new versions of its elements.

The script does not change GUID tables (step 3: put changed tables in bdqtest-graph-inputs/ of the
release by hand), and does not process. Then, from process/:

    python bdq-revisions/bdqtest_elements_to_rs.py            # step 4
    git status                                                 # only the new release directory
    python process.py --config bdq-revisions/bdq-revisions-<date>/config.yaml --dry-run   # on bdq

Usage, from process/:
    python bdq-revisions/bdq_new_release.py <date> --bdqtest <proposals.csv>
        [--substantive <uuid> ...] [--modified-document <document IRI> ...] [--comment <text>]
        [--unchanged-test]

Requires pyyaml.
"""

import argparse
import csv
import datetime
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bdqtest_columns import COLUMNS, HEADER  # noqa: E402

RELEASE_RE = re.compile(r'^bdq-revisions-(\d{4}-\d{2}-\d{2})$')
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
INPUT_COLUMNS = [c for c in HEADER if c in COLUMNS.values()]   # the columns maintainers supply


def fail(message):
    sys.exit('bdq_new_release.py: ' + message)


def releases():
    """The release directories, oldest first, as (date, path)."""
    found = []
    for name in os.listdir(HERE):
        m = RELEASE_RE.match(name)
        if m and os.path.isfile(os.path.join(HERE, name, 'config.yaml')):
            found.append((m.group(1), os.path.join(HERE, name)))
    return sorted(found)


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def latest_test_rows(release_list):
    """Each Test's row in the latest release that has it, in the release input columns."""
    rows = {}
    for date, path in release_list:
        f = os.path.join(path, 'bdqtest.csv')
        if os.path.isfile(f):
            for row in read_csv(f)[1]:
                rows[row['term_localName']] = ({c: row.get(c, '') for c in INPUT_COLUMNS}, date)
    return rows


def proposed_rows(path):
    header, rows = read_csv(path)
    unknown = [c for c in header if c not in COLUMNS]
    if unknown:
        fail(path + ': columns not in bdqtest_columns.COLUMNS: ' + ', '.join(unknown))
    if 'term_localName' not in header:
        fail(path + ': no term_localName column')
    seen = set()
    for row in rows:
        uuid = row['term_localName']
        if not UUID_RE.match(uuid):
            fail(path + ': term_localName is not a lower-case UUID: ' + repr(uuid))
        if uuid in seen:
            fail(path + ': more than one row for ' + uuid)
        seen.add(uuid)
    return [{COLUMNS[k]: v for k, v in row.items() if COLUMNS[k]} for row in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('date', help='release date, YYYY-MM-DD, after the latest release')
    parser.add_argument('--bdqtest', required=True, help='proposed Test rows, in the published column names')
    parser.add_argument('--substantive', action='append', default=[], metavar='UUID',
                        help='a Test whose change is substantive (dateLastUpdated becomes the release date)')
    parser.add_argument('--modified-document', action='append', default=[], metavar='IRI',
                        help='a document (not a List of Terms) whose content changes in this release')
    parser.add_argument('--comment', default='', help='a line for the header comment of config.yaml')
    parser.add_argument('--unchanged-test', action='store_true',
                        help='accept Test rows with no change (a new version for a change in derived elements)')
    args = parser.parse_args()

    try:
        datetime.date.fromisoformat(args.date)
    except ValueError:
        fail('not a date: ' + args.date)
    release_list = releases()
    if not release_list:
        fail('no release directories in ' + HERE)
    latest_date, latest_path = release_list[-1]
    if args.date <= latest_date:
        fail('the release date must be after the latest release, ' + latest_date)
    target = os.path.join(HERE, 'bdq-revisions-' + args.date)
    if os.path.exists(target):
        fail(target + ' exists')

    current = latest_test_rows(release_list)
    proposals = proposed_rows(args.bdqtest)
    proposed_ids = {p['term_localName'] for p in proposals}
    for uuid in args.substantive:
        if uuid not in proposed_ids:
            fail('--substantive ' + uuid + ' is not in the proposals')

    out_rows, report = [], []
    for p in proposals:
        uuid = p['term_localName']
        if uuid in current:
            base, base_date = current[uuid]
            row = dict(base)
            changed = [c for c in p if c != 'term_localName' and p[c] != base[c]]
            given = p.get('dateLastUpdated')
            if given and given not in (base['dateLastUpdated'], args.date):
                fail(uuid + ': DateLastUpdated ' + given + ' is neither the current one, '
                     + base['dateLastUpdated'] + ', nor the release date')
            row.update(p)
            substantive = uuid in args.substantive or given == args.date
            row['dateLastUpdated'] = args.date if substantive else base['dateLastUpdated']
            changed = [c for c in changed if c != 'dateLastUpdated']
            if not changed and not substantive and not args.unchanged_test:
                fail(uuid + ' (' + base['label'] + '): no change from its row in release ' + base_date)
            report.append('%s %s: from release %s; changed %s; dateLastUpdated %s (%s)' % (
                uuid, row['label'], base_date, ', '.join(changed) or 'nothing else',
                row['dateLastUpdated'], 'substantive' if substantive else 'not substantive'))
        else:
            missing = [c for c in INPUT_COLUMNS if c not in p and c != 'dateLastUpdated']
            if missing:
                fail(uuid + ' is a new Test, and the proposal lacks ' + ', '.join(missing))
            row = {c: p.get(c, '') for c in INPUT_COLUMNS}
            row['dateLastUpdated'] = args.date
            report.append('%s %s: new Test' % (uuid, row['label']))
        out_rows.append(row)

    # config.yaml: the latest release's, for the new date.
    with open(os.path.join(latest_path, 'config.yaml'), encoding='utf-8') as f:
        config = yaml.safe_load(f)
    config['date_issued'] = args.date
    config['release_directory'] = config['revision_directory'] + '/bdq-revisions-' + args.date
    list_iris = {v.get('list_of_terms_iri') for v in config.get('vocabularies', [])}
    declared = {d['document'] for d in config.get('documents', [])}
    for iri in args.modified_document:
        if iri not in declared:
            fail('--modified-document ' + iri + ' is not a document in ' + latest_path + '/config.yaml')
        if iri in list_iris:
            fail('--modified-document ' + iri + ' is a List of Terms; it is versioned with its vocabulary')
    for d in config.get('documents', []):
        d.pop('modified', None)
        if d['document'] in args.modified_document:
            d['modified'] = True

    os.mkdir(target)
    comment = ['# BDQ release %s for bdq-public-review.rs.tdwg.org (tdwg/bdq#340).' % args.date]
    if args.comment:
        comment.append('# ' + args.comment)
    comment += ['# Created by bdq_new_release.py from release %s.' % latest_date,
                '# Run with: python process.py --config bdq-revisions/bdq-revisions-%s/config.yaml' % args.date,
                '# Placeholders for the public review: standard YYY, decision_number YYY (plan 8.2.1).']
    with open(os.path.join(target, 'config.yaml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(comment) + '\n')
        f.write(yaml.safe_dump(config, sort_keys=False, allow_unicode=True, width=100000))

    for name in sorted(os.listdir(latest_path)):
        if name.endswith('.csv') and name != 'bdqtest.csv':
            header = read_csv(os.path.join(latest_path, name))[0]
            write_csv(os.path.join(target, name), header, [])
    write_csv(os.path.join(target, 'bdqtest.csv'), INPUT_COLUMNS, out_rows)

    print('Wrote ' + target)
    for line in report:
        print('  ' + line)
    if args.modified_document:
        print('  modified documents: ' + ', '.join(args.modified_document))
    print('Next, from process/: python bdq-revisions/bdqtest_elements_to_rs.py, then git status, '
          'then (on bdq) process.py --config ... --dry-run (README.md, "Changing a Test").')


if __name__ == '__main__':
    main()
