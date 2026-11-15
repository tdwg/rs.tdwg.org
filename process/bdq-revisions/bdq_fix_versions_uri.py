"""One-time fix of versions_uri in the BDQ rows of term-lists/term-lists.csv.

FOR THE BDQ PUBLIC REVIEW (tdwg/bdq#340). versions_uri is meant to be the base of a term list's
version IRIs (e.g. http://rs.tdwg.org/dwc/version/terms/): html:find-version-for-list appends
list_modified to it for "This version" on the term list page. process.py (since 91a2e897) wrote the
IRI of the list's first version instead, so the pages showed two dates run together (e.g.
https://rs.tdwg.org/bdqval/version/terms/2026-04-222026-11-12). process.py and extension_lists.py
on bdq-source now write the base for new term lists; this script corrects the rows written before
that fix, so that the table is what a rerun of every release would produce.

Only rows whose list IRI starts with https://rs.tdwg.org/bdq are changed; the same problem in
other term lists is for the rs.tdwg.org maintainers to fix on master. Idempotent.

Usage, from process/ on bdq:  python bdq-revisions/bdq_fix_versions_uri.py
"""

import csv
import re

PATH = '../term-lists/term-lists.csv'
DATED = re.compile(r'^(.*/)\d{4}-\d{2}-\d{2}$')

with open(PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))
col = {name: i for i, name in enumerate(rows[0])}
fixed = 0
for row in rows[1:]:
    m = DATED.match(row[col['versions_uri']])
    if row[col['list']].startswith('https://rs.tdwg.org/bdq') and m:
        print(row[col['list']] + ': ' + row[col['versions_uri']] + ' -> ' + m.group(1))
        row[col['versions_uri']] = m.group(1)
        fixed += 1
if fixed:
    with open(PATH, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)
print('%d rows fixed' % fixed)
