"""Vocabulary extension term lists (TDWG Standards Documentation Specification, 4.4.2.2).

A vocabulary extension term list holds axioms about terms of a vocabulary that cannot
be rows of a term list, because they need blank nodes (owl:Restriction,
owl:AllDisjointClasses, owl:AllDifferent, ...). It is a term list in its own right
(SDS 2.2.3, 3.3.3): it has its own IRI, is part of its vocabulary, has dated versions,
and lists its distributions (SDS 2.2.4; as rs.tdwg.org does for Documents, the access URL
is the distribution's IRI, rather than an ac:accessURI as in SDS 4.4.3). See process-ontology.md, Section 4.

A vocabulary in config.yaml declares its extension term lists with:

    extension_lists:
    - list_uri: https://rs.tdwg.org/bdqffdq/extension/
      label: ...
      description: ...
      database: bdqffdq                  # dataset directory that holds the axioms file
      axioms_file: bdqffdq-axioms.ttl    # in the release directory when the axioms change
      distribution_base_url: https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/
      browser_redirect: https://...       # optional: human-readable document for HTML requests

When the release directory contains the axioms file and its axioms differ from the
current ones (or the list is new), this step:

- writes the current axioms to <database>/<database>-axioms.{ttl,rdf,jsonld} and an
  immutable copy for the version to <database>/axioms-versions/<database>-axioms-<date>.*;
- writes the current term list row (term-lists.csv), its members (the terms of the
  vocabulary that the axioms are about), its distributions (term-lists-formats.csv,
  following docs/docs-formats.csv: dcterms:hasFormat, dc:format, foaf:Document);
- writes the term list version (term-lists-versions.csv), its members (the term versions
  applicable on the release date), its replacement of the previous version, and its
  distributions (term-lists-versions-formats.csv);
- returns what the release loop needs to update the vocabulary and standard versions.

Unchanged axioms create nothing, and a same-release rerun rewrites the version of that
date in place. Requires rdflib.
"""
import datetime
import os
import subprocess
import sys
import urllib.parse

FORMATS = (('ttl', 'turtle', 'text/turtle', 'RDF/Turtle'),
           ('rdf', 'xml', 'application/rdf+xml', 'RDF/XML'),
           ('jsonld', 'json-ld', 'application/ld+json', 'JSON-LD'))


def _rdflib():
    try:
        import rdflib
        import rdflib.compare
        return rdflib
    except ImportError:
        raise SystemExit('Vocabulary extension term lists require rdflib (see requirements.txt).')


def term_list_version_iri(list_uri, date_issued):
    """Same convention as for term lists: insert 'version' after the first path component."""
    parts = urllib.parse.urlsplit(list_uri)
    path = [p for p in parts.path.split('/') if p]
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, '/' + '/'.join([path[0], 'version'] + path[1:] + [date_issued]), '', ''))


def _local_name(list_uri):
    return urllib.parse.urlsplit(list_uri).path.lstrip('/')


def _write_axioms(rdflib, graph, list_uri, version_iri, base_path):
    """Writes <base_path>.ttl/.rdf/.jsonld with owl:versionIRI in the list's header; deterministic."""
    from rdflib.compare import to_canonical_graph
    from rdflib.namespace import OWL, RDF
    out = rdflib.Graph()
    for triple in sorted(to_canonical_graph(graph)):
        out.add(triple)
    for prefix, namespace in graph.namespaces():
        out.bind(prefix, namespace, override=True, replace=True)
    subject = rdflib.URIRef(list_uri)
    out.add((subject, RDF.type, OWL.Ontology))
    out.remove((subject, OWL.versionIRI, None))
    out.add((subject, OWL.versionIRI, rdflib.URIRef(version_iri)))
    os.makedirs(os.path.dirname(base_path), exist_ok=True)
    out.serialize(base_path + '.ttl', format='turtle')
    # rdflib's RDF/XML and JSON-LD writers iterate over sets, so their order depends on
    # the string hash seed; write them from the Turtle in a process with a fixed seed.
    script = (
        'import json, sys, rdflib\n'
        'from rdflib.compare import to_canonical_graph\n'
        'base = sys.argv[1]\n'
        'parsed = rdflib.Graph().parse(base + ".ttl", format="turtle")\n'
        'g = rdflib.Graph()\n'
        'for t in sorted(to_canonical_graph(parsed)): g.add(t)\n'
        'for p, n in parsed.namespaces(): g.bind(p, n, override=True, replace=True)\n'
        'g.serialize(base + ".rdf", format="xml")\n'
        'def ordered(v):\n'
        '    if isinstance(v, dict): return {k: ordered(x) for k, x in v.items()}\n'
        '    if isinstance(v, list): return sorted((ordered(x) for x in v), key=lambda x: json.dumps(x, sort_keys=True))\n'
        '    return v\n'
        'data = ordered(json.loads(g.serialize(format="json-ld")))\n'
        'open(base + ".jsonld", "w", encoding="utf-8").write(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\\n")\n'
    )
    subprocess.run([sys.executable, '-c', script, base_path], check=True,
                   env=dict(os.environ, PYTHONHASHSEED='0'))


def _read(read_csv, path, header):
    if os.path.exists(path):
        return read_csv(path)
    return [header]


def _members(rdflib, graph, term_iris):
    found = set()
    for triple in graph:
        for node in triple:
            if isinstance(node, rdflib.URIRef) and str(node) in term_iris:
                found.add(str(node))
    return sorted(found)


def _applicable_term_versions(read_csv, database, member_iris, namespace_uri, date_issued):
    """The term version of each member applicable on date_issued (latest issued on or before it)."""
    versions = read_csv(os.path.join('..', database + '-versions', database + '-versions.csv'))
    header = versions[0]
    v_col, date_col, local_col = header.index('version'), header.index('version_issued'), header.index('term_localName')
    target = datetime.date.fromisoformat(date_issued)
    best = {}
    for row in versions[1:]:
        term = namespace_uri + row[local_col]
        issued = datetime.date.fromisoformat(row[date_col])
        if term in member_iris and issued <= target and (term not in best or issued > best[term][0]):
            best[term] = (issued, row[v_col])
    missing = sorted(set(member_iris) - set(best))
    if missing:
        raise ValueError('Axioms refer to terms with no version on or before ' + date_issued + ': ' + ', '.join(missing))
    return [best[t][1] for t in sorted(best)]


def process_extension_list(ext, vocabulary_namespaces, ctx):
    """Processes one extension term list. Returns (changed, term_lists_table, row_number, version_iri, is_new)."""
    rdflib = _rdflib()
    read_csv, write_csv, iso_time = ctx['readCsv'], ctx['writeCsv'], ctx['isoTime']
    date_issued, offset = ctx['date_issued'], ctx['local_offset_from_utc']
    list_uri, database = ext['list_uri'], ext['database']
    release_axioms = os.path.join(ctx['release_directory'], ext['axioms_file'])
    current_base = os.path.join('..', database, database + '-axioms')
    version_iri = term_list_version_iri(list_uri, date_issued)

    term_lists = read_csv('../term-lists/term-lists.csv')
    h = term_lists[0]
    col = {name: h.index(name) for name in h}
    rows = [n for n in range(1, len(term_lists)) if term_lists[n][col['list']] == list_uri]
    is_new = not rows

    if not os.path.exists(release_axioms):
        if is_new:
            raise ValueError('New extension term list ' + list_uri + ' has no axioms file ' + release_axioms)
        return False, term_lists, rows[0], None, False

    graph = rdflib.Graph().parse(release_axioms, format='turtle')
    tlv = read_csv('../term-lists-versions/term-lists-versions.csv')
    th = tlv[0]
    tcol = {name: th.index(name) for name in th}
    earlier = [r for r in tlv[1:] if r[tcol['list']] == list_uri and r[tcol['version_modified']] < date_issued]
    same_date = [r for r in tlv[1:] if r[tcol['list']] == list_uri and r[tcol['version_modified']] == date_issued]
    if not is_new and not same_date and os.path.exists(current_base + '.ttl'):
        current = rdflib.Graph().parse(current_base + '.ttl', format='turtle')
        current.remove((rdflib.URIRef(list_uri), rdflib.namespace.OWL.versionIRI, None))
        compare = rdflib.Graph()
        for t in graph:
            compare.add(t)
        compare.add((rdflib.URIRef(list_uri), rdflib.namespace.RDF.type, rdflib.namespace.OWL.Ontology))
        if rdflib.compare.isomorphic(current, compare):
            return False, term_lists, rows[0], None, False

    # Members: the terms of the vocabulary's term lists that the axioms are about.
    term_iris = {}
    for namespace in vocabulary_namespaces:
        if namespace.get('utility_namespace') or namespace.get('borrowed'):
            continue
        db = namespace['database']
        terms = read_csv(os.path.join('..', db, db + '.csv'))
        local = terms[0].index('term_localName')
        for row in terms[1:]:
            term_iris[namespace['namespace_uri'] + row[local]] = (db, namespace['namespace_uri'])
    members = _members(rdflib, graph, term_iris)
    if not members:
        raise ValueError('Extension term list ' + list_uri + ': the axioms refer to no term of the vocabulary.')
    member_versions = []
    for db, ns in sorted(set(term_iris[m] for m in members)):
        member_versions += _applicable_term_versions(read_csv, db, [m for m in members if term_iris[m] == (db, ns)], ns, date_issued)

    # Axioms files: current, and an immutable copy for this version.
    version_base = os.path.join('..', database, 'axioms-versions', database + '-axioms-' + date_issued)
    _write_axioms(rdflib, graph, list_uri, version_iri, current_base)
    _write_axioms(rdflib, graph, list_uri, version_iri, version_base)

    # Current term list row.
    local_name = _local_name(list_uri)
    now = iso_time(offset)
    if is_new:
        row = [''] * len(h)
        row[col['list_created']] = date_issued
        term_lists.append(row)
        row_number = len(term_lists) - 1
    else:
        row_number = rows[0]
        row = term_lists[row_number]
    for name, value in (('document_modified', now), ('list', list_uri), ('list_localName', local_name),
                        ('label', ext['label']), ('description', ext['description']), ('list_modified', date_issued),
                        ('versions_uri', version_iri), ('standard', ctx['standardUri'])):
        if name in col:
            row[col[name]] = value
    write_csv('../term-lists/term-lists.csv', term_lists)

    # Current members (the vocabulary's terms the axioms are about).
    tlm = read_csv('../term-lists/term-lists-members.csv')
    tlm = [tlm[0]] + [r for r in tlm[1:] if r[0] != list_uri] + [[list_uri, m] + [''] * (len(tlm[0]) - 2) for m in members]
    write_csv('../term-lists/term-lists-members.csv', tlm)

    # Term list version: replace a same-date version (rerun), otherwise add one.
    tlv = [tlv[0]] + [r for r in tlv[1:] if not (r[tcol['list']] == list_uri and r[tcol['version_modified']] == date_issued)]
    vrow = [''] * len(th)
    for name, value in (('document_modified', now), ('version', version_iri), ('version_modified', date_issued),
                        ('status', 'recommended'), ('list_localName', local_name), ('label', ext['label']),
                        ('description', ext['description']), ('list_created', row[col['list_created']]),
                        ('list_modified', date_issued), ('list', list_uri)):
        if name in tcol:
            vrow[tcol[name]] = value
    tlv.append(vrow)
    write_csv('../term-lists-versions/term-lists-versions.csv', tlv)

    tlvm = read_csv('../term-lists-versions/term-lists-versions-members.csv')
    tlvm = [tlvm[0]] + [r for r in tlvm[1:] if r[0] != version_iri] + [[version_iri, v] for v in member_versions]
    write_csv('../term-lists-versions/term-lists-versions-members.csv', tlvm)

    previous = max(earlier, key=lambda r: r[tcol['version_modified']])[tcol['version']] if earlier else None
    replacements = read_csv('../term-lists-versions/term-lists-versions-replacements.csv')
    replacements = [replacements[0]] + [r for r in replacements[1:] if r[0] != version_iri]
    if previous:
        replacements.append([version_iri, previous])
    write_csv('../term-lists-versions/term-lists-versions-replacements.csv', replacements)

    # Join of the list and its versions (dcterms:hasVersion), as for any term list.
    joins = read_csv('../term-lists/term-lists-versions.csv')
    joins = [joins[0]] + [r for r in joins[1:] if r[0] != version_iri] + [[version_iri, list_uri]]
    write_csv('../term-lists/term-lists-versions.csv', joins)

    # Axioms files of the list and its versions, which rs.tdwg.org appends to their RDF (restxq.xqm).
    axioms_lookup = _read(read_csv, '../term-lists/term-lists-axioms.csv', ['iri', 'file'])
    axioms_lookup = [axioms_lookup[0]] + [r for r in axioms_lookup[1:] if r[0] not in (list_uri, version_iri)]
    axioms_lookup += [[list_uri, database + '/' + database + '-axioms'],
                      [version_iri, database + '/axioms-versions/' + database + '-axioms-' + date_issued]]
    write_csv('../term-lists/term-lists-axioms.csv', axioms_lookup)

    # Browser redirect of the list and its versions to the human-readable document (SDS 3.3.3).
    if ext.get('browser_redirect'):
        redirects = _read(read_csv, '../term-lists/term-lists-redirects.csv', ['iri', 'redirect'])
        redirects = [redirects[0]] + [r for r in redirects[1:] if r[0] not in (list_uri, version_iri)]
        redirects += [[list_uri, ext['browser_redirect']], [version_iri, ext['browser_redirect']]]
        write_csv('../term-lists/term-lists-redirects.csv', redirects)

    # Distributions (SDS 2.2.4), following current TDWG practice for Document distributions
    # (docs/docs-formats.csv): dcterms:hasFormat to the access URL, typed foaf:Document,
    # with dc:format. The version's distributions are the immutable per-version files.
    base_url = ext['distribution_base_url'].rstrip('/') + '/'
    for path, link_column, subject, base in (
            ('../term-lists/term-lists-formats.csv', 'termList', list_uri, database + '/' + database + '-axioms'),
            ('../term-lists-versions/term-lists-versions-formats.csv', 'termListVersion', version_iri,
             database + '/axioms-versions/' + database + '-axioms-' + date_issued)):
        table = _read(read_csv, path, [link_column, 'mediaType', 'accessUri'])
        table = [table[0]] + [r for r in table[1:] if r[0] != subject]
        for ext_, _, media_type, _ in FORMATS:
            table.append([subject, media_type, base_url + base + '.' + ext_])
        write_csv(path, table)

    return True, term_lists, row_number, version_iri, is_new
