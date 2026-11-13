"""Declare the BDQ documents other than the Lists of Terms in a BDQ release.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340), like bdq_to_rs.py, and intended
to be replaced by the authoritative inputs kept in this repository: after it
has run, the `documents` entries in the release config.yaml are the source and
are edited in place.

Plan Section 11 (decided 2026-11-12): document IRIs are
https://rs.tdwg.org/{vocabulary}/doc/{name}/ for documents about one vocabulary
and https://rs.tdwg.org/bdq/doc/{name}/ for the others; the Quick Reference
Guide is one document (its term descriptions and index pages are supporting
parts of it); the index of normative sections is not a document; the landing
page is covered by the standard record; on the review site each document has
only its latest version, so the documents are declared only in the last release.
Decided 2026-11-13: that release is bdq-revisions-2026-11-13, in which the documents
are first issued (they had been declared in bdq-revisions-2026-11-09).

The metadata come from tg2/_build_review/templates/*/document_configuration.yaml
in tdwg/bdq and the shared tg2/_build_review/authors_configuration.yaml. Their
current_iri, dcterms_isPartOf, doc_created, and doc_modified are not used
(process.py sets the standard and the dates). accessUrl and browserRedirectUri
are derived from the published location of each document in tg2/_review/,
because several drafts have inconsistent or wrong values; browserRedirectUri is
the current /draft/ location, PROVISIONAL like that of the Lists of Terms (plan
Section 8.6). The publisher and license come from document_defaults, as for the
Lists of Terms; other values equal to document_defaults are left out.

Usage: python -I bdq_docs_to_rs.py <bdq_repo> <release config.yaml>
"""
import pathlib, sys
import yaml

bdq, config_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

# (template directory, document IRI, published path under tg2/_review/)
DOCUMENTS = [
    ('bdqffdq', 'https://rs.tdwg.org/bdqffdq/doc/ontology/', 'docs/bdqffdq'),
    ('extension/bdqffdq', 'https://rs.tdwg.org/bdqffdq/doc/extension/', 'docs/extension/bdqffdq'),
    ('guide/bdqffdq', 'https://rs.tdwg.org/bdqffdq/doc/guide/', 'docs/guide/bdqffdq'),
    ('guide/bdqtest', 'https://rs.tdwg.org/bdqtest/doc/guide/', 'docs/guide/bdqtest'),
    ('terms/bdqtest_qrg', 'https://rs.tdwg.org/bdqtest/doc/qrg/', 'docs/terms/bdqtest'),
    ('guide/implementers', 'https://rs.tdwg.org/bdq/doc/implementers/', 'docs/guide/implementers'),
    ('guide/users', 'https://rs.tdwg.org/bdq/doc/users/', 'docs/guide/users'),
    ('guide/synthetic', 'https://rs.tdwg.org/bdq/doc/synthetic/', 'docs/guide/synthetic'),
    ('supplement', 'https://rs.tdwg.org/bdq/doc/supplement/', 'docs/supplement'),
    ('tutorial', 'https://rs.tdwg.org/bdq/doc/tutorial/', 'docs/tutorial'),
]
ACCESS_BASE = 'https://raw.githubusercontent.com/tdwg/bdq/master/tg2/_review/'
REDIRECT_BASE = 'https://bdq.tdwg.org/draft/'          # PROVISIONAL (plan Section 8.6)
KEPT = ('documentTitle', 'abstract', 'creator', 'mediaType', 'comment')   # publisher and license: document_defaults, as for the Lists of Terms

text = config_path.read_text(encoding='utf-8')
header = ''.join(l for l in text.splitlines(True) if l.startswith('#'))
config = yaml.safe_load(text[len(header):])
defaults = config.get('document_defaults') or {}
contributors = yaml.safe_load(open(bdq / 'tg2/_build_review/authors_configuration.yaml', encoding='utf-8'))
for c in contributors:
    for k in ('contributor_iri', 'contributor_literal', 'contributor_role', 'role_uri', 'affiliation', 'affiliation_uri'):
        c[k] = '' if c.get(k) is None else str(c[k])

ours = {iri for _, iri, _ in DOCUMENTS}
documents = [d for d in config['documents'] if d['document'] not in ours]   # rerunnable
for template, iri, path in DOCUMENTS:
    if not (bdq / 'tg2/_review' / path / 'index.md').is_file():
        sys.exit(f'no published document at tg2/_review/{path}/index.md')
    source = yaml.safe_load(open(bdq / 'tg2/_build_review/templates' / template / 'document_configuration.yaml', encoding='utf-8'))
    entry = {'document': iri}
    for k in KEPT:
        if k in source and source[k] is not None and str(source[k]) != str(defaults.get(k)):
            entry[k] = str(source[k]).strip()
    entry['accessUrl'] = ACCESS_BASE + path + '/index.md'
    entry['browserRedirectUri'] = REDIRECT_BASE + path + '/'
    entry['contributors'] = contributors
    documents.append(entry)
    print(iri, '<-', template)
config['documents'] = documents


class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


config_path.write_text(header + yaml.dump(config, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')
