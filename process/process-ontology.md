# Describing an ontology in rs.tdwg.org

This document describes how a TDWG vocabulary that is an OWL ontology is kept in rs.tdwg.org, and how `process/build_ontology.py` generates the ontology from it. It complements [`process-vocabulary.md`](process-vocabulary.md), which describes the release processing that every vocabulary goes through.

The first ontology described this way is the BDQ Fitness For Use Framework ontology (`bdqffdq`). Its inputs are in `process/bdq-revisions/` (on the BDQ branches), and the design is discussed in [tdwg/bdq#340](https://github.com/tdwg/bdq/issues/340) and in the plan [`tg2/_make_review/deployment_rs_tdwg_org.md`](https://github.com/tdwg/bdq/blob/master/tg2/_make_review/deployment_rs_tdwg_org.md), Section 9.5.

## 1 Three parts

rs.tdwg.org describes named resources with tables: one row per term, one column per property. Most of an ontology fits that model: the type, labels, and definition of each class, property, and named individual, and the statements that link named terms (`rdfs:subClassOf`, `rdfs:subPropertyOf`, a named `rdfs:range`). What does not fit are axioms that need blank nodes: class expressions such as `owl:Restriction`, and n-ary axioms such as `owl:AllDisjointClasses` or `owl:AllDifferent`. In OWL 2 DL these nodes must be blank, so they cannot be given IRIs and stored as rows.

Following the layered approach of the [TDWG Standards Documentation Specification](http://rs.tdwg.org/sds/doc/specification/) (SDS), Section 4.4.2.2 (*Vocabulary extension term lists*), an ontology is therefore described in three parts:

| Part | Where | SDS role |
|---|---|---|
| **Basic term list**: one row per term | the dataset's current-terms CSV (e.g. `bdqffdq/bdqffdq.csv`) and its column mappings, processed by `process.py` | basic term list; not itself declared an `owl:Ontology` |
| **Axioms file**: the axioms that need blank nodes | an input in the release directory; `process.py` records it as an extension term list (Section 4) and writes `<dataset>/<dataset>-axioms.{ttl,rdf,jsonld}` | vocabulary extension term list, typed `owl:Ontology` |
| **Vocabulary record**: the ontology header | `vocabularies/`, `vocabularies-versions/`, written by `process.py` from `config.yaml` | the vocabulary that combines the two; its IRI is the ontology IRI |

The terms get the same treatment as the terms of any other vocabulary: term versions, dereferencing, content negotiation, and redirects to the human-readable List of Terms. A term-level response from rs.tdwg.org carries everything in the term's row, but not the axioms in the axioms file; those are delivered by the extension term list (Section 4).

## 2 Preparing the inputs

### 2.1 The term list

The term list is an ordinary namespace in `config.yaml` (Section 3.3 of `process-vocabulary.md`), usually with `vocab_type: 1`, and an ordinary release-input CSV. Add columns for the statements about named terms, and edit the column mappings (Section 3.10 of `process-vocabulary.md`). Repeated properties use repeated columns mapped to the same predicate, for example:

| header | predicate | type |
|---|---|---|
| `type`, `type1` | `rdf:type` | `iri` |
| `subClassOf`, `subClassOf1`, `subClassOf2` | `rdfs:subClassOf` | `iri` |
| `subPropertyOf`, `subPropertyOf1` | `rdfs:subPropertyOf` | `iri` |
| `range` | `rdfs:range` | `iri` (named classes and datatypes only) |
| `controlled_value_string` | `rdf:value` and `skos:notation` | `plain` |

IRI cells hold full IRIs or CURIEs whose prefixes are in the dataset's `namespace.csv`.

Every term needs an `rdf:type` (`owl:Class`, `owl:ObjectProperty`, `owl:DatatypeProperty`, `owl:AnnotationProperty`, `owl:NamedIndividual` and the individual's class, …).

**Controlled value strings.** SDS Section 4.5.4 designates the unique string of a controlled vocabulary term with `rdf:value`. `rdf:value` is reserved vocabulary in OWL 2 and cannot be used as an annotation property in OWL 2 DL. Keep `rdf:value` in the term list, so that term-level responses follow the SDS, and map the same column to `skos:notation` as well. The generator leaves `rdf:value` out of the ontology (Section 3).

### 2.2 The axioms file

The axioms file is a Turtle file with:

- its own ontology header: the extension term list's IRI, typed `owl:Ontology`, with an `rdfs:label`;
- the axioms that need blank nodes, about terms of the term list.

For example:

```turtle
@prefix bdqffdq: <https://rs.tdwg.org/bdqffdq/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://rs.tdwg.org/bdqffdq/extension/> a owl:Ontology ;
    rdfs:label "Fitness For Use Framework Ontology Vocabulary Extension"@en .

bdqffdq:Validation rdfs:subClassOf [ a owl:Restriction ;
        owl:onProperty bdqffdq:hasCriterion ;
        owl:allValuesFrom bdqffdq:Criterion ] .

[] a owl:AllDisjointClasses ;
    owl:members ( bdqffdq:Amendment bdqffdq:Issue bdqffdq:Measure bdqffdq:Validation ) .
```

Statements that can be rows belong in the term list, not in the axioms file. Put the axioms file in the release directory of each release in which the axioms change, and declare the extension term list in `config.yaml` (Section 4).

Validation rules that express expectations about data (cardinalities, "SHOULD have"), rather than definitions, are better kept out of the ontology and checked with SHACL: OWL axioms are absolute, and under the open world assumption they do not report missing or extra values.

### 2.3 The vocabulary record

The vocabulary in `config.yaml` that contains the term list provides the ontology header. Its `vocabulary` IRI is the ontology IRI, and its current version IRI is the `owl:versionIRI`. Give it the ontology's label (`vocabulary_label`), description (`vocabulary_description`), creator, and license.

## 3 Generating the ontology

After processing (Section 3.5 of `process-vocabulary.md`) and copying the axioms file into the dataset directory, run from the `process` directory:

```bash
python build_ontology.py ../bdqffdq --output-dir /path/to/output
```

This writes `bdqffdq.ttl`, `bdqffdq.rdf` (RDF/XML), and `bdqffdq.jsonld` to the output directory. The files are not committed to rs.tdwg.org: the standard's own build publishes them (for BDQ, in `tg2/_review/dist/` of tdwg/bdq), while rs.tdwg.org serves the individual terms.

The generator:

1. makes the statements about each term from the current-terms CSV and its column mappings, with the same rules as the rs.tdwg.org serializer (`html/restxq.xqm`), so that the ontology and the term-level responses agree. Rows of linked resources (versions, replacements) are not included;
2. adds the axioms file, without its ontology header;
3. writes the ontology header from the vocabulary record: `owl:Ontology`, `owl:versionIRI` (the current vocabulary version), `rdfs:label`, `dcterms:description`, `dcterms:creator`, `dcterms:license`, `dcterms:issued` (the version date), and `dcterms:hasPart` the term list and the extension term list;
4. replaces annotations with reserved properties that OWL 2 DL does not allow, by default `rdf:value` with `skos:notation`. A replacement that duplicates an existing statement is dropped. The header's `rdfs:comment` records the replacement;
5. declares every annotation property it uses, and every datatype outside the OWL 2 datatype map (e.g. `xsd:date`, used for `dcterms:created`);
6. checks that the axioms file refers only to terms of the term list, and that every term has an `rdf:type`.

The output is deterministic: the same inputs give the same files.

### 3.1 Validation with ROBOT

[ROBOT](http://robot.obolibrary.org/) (BSD-3-Clause, built on the OWL API) is an optional dependency. With ROBOT, the generator also checks that the ontology is in the OWL 2 DL profile and consistent (HermiT reasoner), and the Turtle and RDF/XML files are written by the OWL API. Without ROBOT, rdflib writes all three files and the generator reports that the ontology was not validated.

ROBOT is distributed as a jar (Java 11 or later) from its GitHub releases, and as Docker images (`obolibrary/robot`, `obolibrary/odkfull`). The generator finds it with `--robot /path/to/robot.jar`, the `ROBOT_JAR` environment variable, or a `robot` command on the `PATH`; `--no-robot` skips it.

```bash
python build_ontology.py ../bdqffdq --output-dir /path/to/output --robot /path/to/robot.jar
```

Requires `rdflib` (in `requirements.txt`).

## 4 The extension term list

The axioms file is a vocabulary extension term list (SDS 2.2.3, 3.3.3, 4.4.2.2): a term list with its own IRI, part of its vocabulary, with dated versions and distributions. Declare it under its vocabulary in `config.yaml`:

```yaml
  extension_lists:
  - list_uri: https://rs.tdwg.org/bdqffdq/extension/
    label: Fitness For Use Framework Ontology Vocabulary Extension
    description: Axioms about bdqffdq terms that need blank nodes ...
    database: bdqffdq                  # dataset directory for the axioms files
    axioms_file: bdqffdq-axioms.ttl    # in the release directory when the axioms change
    distribution_base_url: https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/
    browser_redirect: https://...       # the human-readable document, for HTML requests
```

Declare it from the first release that contains the axioms file. In each release whose directory contains the axioms file, `process.py` (with `extension_lists.py`) compares the axioms with the current ones. If they differ, or the list is new, it:

- writes the current axioms, with `owl:versionIRI`, to `<database>/<database>-axioms.{ttl,rdf,jsonld}`, and an immutable copy for the version to `<database>/axioms-versions/<database>-axioms-<date>.{ttl,rdf,jsonld}`;
- writes the term list record (`term-lists/term-lists.csv`) and its members (`term-lists-members.csv`): the vocabulary's terms that the axioms are about, as for a list of borrowed terms;
- writes the term list version (`term-lists-versions/term-lists-versions.csv`, e.g. `https://rs.tdwg.org/bdqffdq/version/extension/2026-11-09`), its members (the term versions applicable on the release date), and its replacement of the previous version;
- writes the distributions (`term-lists/term-lists-formats.csv`, `term-lists-versions/term-lists-versions-formats.csv`), following rs.tdwg.org's practice for Document distributions (`docs/docs-formats.csv`): `dcterms:hasFormat` to the access URL, typed `foaf:Document`, with `dc:format`. The access URL is the distribution's IRI; SDS 4.4.3 suggests `ac:accessURI`, which rs.tdwg.org does not use;
- adds the extension term list to the vocabulary and creates the vocabulary and standard versions, as for any term list.

The extension term list then dereferences like any term list, with `dcterms:hasVersion` to its versions. HTML requests for the list and its versions redirect to `browser_redirect` (`term-lists/term-lists-redirects.csv`; SDS 3.3.3: the human-readable representation of an extension list is a separate document). Its RDF (Turtle, RDF/XML, JSON-LD), for the list and for each version, is its metadata from the tables followed by its axioms: `term-lists/term-lists-axioms.csv` gives the axioms files of each extension list IRI, and `html/restxq.xqm` appends them (`page:with-axioms`). So `owl:imports <https://rs.tdwg.org/bdqffdq/extension/>` retrieves the axioms from rs.tdwg.org, and a version IRI retrieves that version's axioms. The axioms files are also listed as distributions. The term list record is typed `tdwgutility:TermList`; the axioms type the list `owl:Ontology`. Unchanged axioms create no version, and a same-release rerun rewrites the version of that date. A release can declare the list without an axioms file when the axioms do not change. The axioms files are written deterministically.
