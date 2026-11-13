"""The columns of the bdqtest release inputs, shared by bdqtest_to_rs.py and bdqtest_graphs.py.

FOR THE BDQ PUBLIC REVIEW ONLY (tdwg/bdq#340). COLUMNS maps the columns of tdwg/bdq
tg2/_review/vocabulary/bdqtest_term_versions.csv to the columns of the rs.tdwg.org bdqtest
term list (legal XML names); it is also the mapping back to the published names (plan
Section 10.8). DERIVED are the columns that hold the IRIs on the Test node.
"""

# Published column -> rs.tdwg.org column (Section 10.8). None: derived by rs.tdwg.org, not an input.
COLUMNS = {
    'term_localName': 'term_localName',
    'Label': 'label',
    'prefLabel': 'prefLabel',
    'definition': 'definition',
    'Description': 'description',
    'Notes': 'notes',
    'historyNoteUrl': 'historyNoteUrl',
    'issueNumber': 'issueNumber',
    'DateLastUpdated': 'dateLastUpdated',
    'Type': 'testType',
    'Resource Type': 'resourceType',
    'Dimension': 'dimension',
    'Criterion': 'criterion',
    'Enhancement': 'enhancement',
    'IE Class': 'ieClass',
    'InformationElement:ActedUpon': 'informationElementActedUpon',
    'InformationElement:Consulted': 'informationElementConsulted',
    'aggregatesResponsesFrom': 'aggregatesResponsesFrom',
    'Parameters': 'parameters',
    'ExpectedResponse': 'expectedResponse',
    'AuthoritiesDefaults': 'authoritiesDefaults',
    'SpecificationGuid': 'specificationGuid',
    'MethodGuid': 'methodGuid',
    'ArgumentGuids': 'argumentGuids',
    'Examples': 'examples',
    'Source': 'source',
    'References': 'references',
    'Example Implementations (Mechanisms)': 'exampleImplementations',
    'Link to Specification Source Code': 'specificationSourceCode',
    'IssueState': 'issueState',
    'IssueLabels': 'issueLabels',
    'UseCases': 'useCases',
    'status': 'bdqStatus',
    'flags': 'flags',
    'organized_in': 'organizedIn',
    'iri': None,        # the version IRI: rs.tdwg.org mints it from the release date
    'term_iri': None,   # the term IRI: namespace + term_localName
    'issued': None,     # the version's release date
}
# Derived columns: the IRIs that BDQ's RDF puts on the Test node (build_bdqtest_rdf.py).
DERIVED = ['type', 'hasResourceType', 'hasDataQualityDimension', 'hasCriterion', 'hasEnhancement']
HEADER = [c for c in COLUMNS.values() if c] + DERIVED
