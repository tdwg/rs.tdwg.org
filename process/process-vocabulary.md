# Processing vocabulary and document changes

**Title:** Processing vocabulary and document changes

**Date Modified:** 2026-10-15

**Part of TDWG Standard:** Not part of any standard

**Abstract:** This document describes the maintainer workflow for processing one complete TDWG standards release into the metadata maintained in `rs.tdwg.org`. The release processor reads a stable `config.yaml` together with release-specific namespace CSV files; validates the complete Standard, Vocabulary, Term List, and Document declaration; stages all generated metadata changes transactionally; supports a non-publishing `--dry-run` preview of the complete release; and publishes the resulting repository delta only after successful normal processing. This document provides a short release recipe followed by detailed explanations of each step and of the metadata resources affected by processing.

**Contributors:** Steve Baskauf (TDWG Technical Architecture Group, TDWG Audiovisual Core Maintenance Group, TDWG Darwin Core Maintenance Group), John Wieczorek (TDWG Darwin Core Maintenance Group)

# Table of Contents

[1 Introduction](#1-introduction)

[2 Release recipe](#2-release-recipe)

[3 Detailed workflow](#3-detailed-workflow)

[4 What `process.py` modifies](#4-what-processpy-modifies)

[5 Building a human-readable List of Terms document](#5-building-a-human-readable-list-of-terms-document)

[6 Generating JSON-LD for controlled vocabularies](#6-generating-json-ld-for-controlled-vocabularies)

[7 Reference](#7-reference)

# 1 Introduction

## 1.1 RFC 2119 statement

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14) [[RFC 2119]](https://datatracker.ietf.org/doc/html/rfc2119) and [[RFC 8174]](https://datatracker.ietf.org/doc/html/rfc8174) when, and only when, they appear in all capitals, as shown here.

Use of RFC 2119 keywords is not an indication that compliance is required by a TDWG standard. Rather, it indicates requirements of the processing software and maintenance workflow described here.

## 1.2 Audience

This document is intended primarily for maintainers of the TDWG `rs.tdwg.org` infrastructure and for Maintenance Group members preparing release inputs. It may also be used by developers who need to generate draft metadata in a fork of `rs.tdwg.org` before ratification.

## 1.3 Scope and current processing model

The [TDWG Standards Documentation Specification](http://rs.tdwg.org/sds/doc/specification/) (SDS) requires human- and machine-readable representations of standard components to be consistent. The authoritative metadata used to generate those representations are maintained in `rs.tdwg.org`.

The current `process.py` is a **release-level processor**. One invocation processes one complete release of one Standard. The release declaration in `process/config.yaml` identifies:

- the release date and Standard;
- every current Vocabulary that is a direct part of that Standard;
- every namespace/Term List belonging to each configured Vocabulary;
- every current Document that is a direct part of the Standard;
- release-specific namespace input CSV files; and
- the Executive Committee decision metadata associated with the release.

A release can therefore contain **multiple Vocabularies** and **multiple Documents**. A separate `vocab.yaml` file is no longer part of this workflow; Vocabulary and Standard release configuration is consolidated in `config.yaml`.

For each configured namespace, a CSV named from its configured namespace prefix is expected in the release revision directory. A CSV containing only its header means that the namespace participates in the release but has no term changes.

`config.yaml` is also the authoritative declaration of **current containment** for processing purposes. Its Vocabulary/namespace structure determines current Term List-to-Vocabulary ownership, and its `documents` list together with the configured Vocabularies determines the current direct composition of the Standard. Dated Vocabulary- and Standard-version membership tables remain historical snapshots and are not templates from which future membership is inferred.

The processor also manages Document metadata from the centralized release declaration in `config.yaml`. Vocabulary-associated Lists-of-Terms Documents are versioned when a member Term List changes or the Vocabulary's current Term List membership changes. Other configured Documents use `modified: true` in their release-level Document declaration as the explicit signal that the Document changed in the target release. Document identity, Standard containment, and lifecycle dates are derived by the processor rather than repeated as maintainer-supplied metadata.

Term deprecations are not supported by the normal workflow described here. See [section 3.11](#311-legacy-notebooks-and-term-deprecations).

# 2 Release recipe

This section is the short recipe. Follow the links for the details and for explanations of the repository resources affected by each operation.

1. **Create or select a working branch and prepare the release directory.** Start from the repository state that should precede the release. A pre-processing commit is RECOMMENDED as a useful checkpoint. See [3.1](#31-create-the-working-branch-and-release-directory).
2. **Prepare one release-input CSV for every configured namespace.** Include only the new or modified terms; use a header-only file when there are no term changes in that namespace. See [3.2](#32-prepare-namespace-release-input-csv-files).
3. **Update `process/config.yaml` for the complete Standard release.** Declare the complete current Vocabulary, namespace/Term List, and Document composition—not only resources that changed. See [3.3](#33-configure-the-complete-release-in-configyaml).
4. **Update the Document declarations in `config.yaml` where necessary.** For a changed non-List-of-Terms Document, set `modified: true` and update its declared metadata or contributors as needed. Do not set `modified` on Vocabulary-associated Lists-of-Terms Documents; their versioning is controlled by Vocabulary/Term List release state. See [3.4](#34-prepare-document-metadata).
5. **Preview the release with `python process.py --dry-run` from the `process` directory.** The complete release is validated and processed in a temporary repository; proposed file creations, modifications, and deletions are reported without publishing metadata, logs, or reports. See [3.5](#35-run-the-processor).
6. **Run `python process.py` when the preview is satisfactory.** The complete release is processed again in staging and the validated metadata delta is published transactionally, followed by its log and report. See [3.5](#35-run-the-processor).
7. **Inspect the generated release carefully.** Review console output, the generated release report, the processing log, `git diff --check`, `git status --short`, `git diff --stat`, and the substantive diff. See [3.6](#36-review-the-generated-release) and [section 4](#4-what-processpy-modifies).
8. **If anything is wrong, correct the authoritative input and preview again before publishing.** The processor is designed to converge on the state represented by the current inputs. An unchanged same-release rerun should produce no additional repository metadata changes. See [3.7](#37-correct-and-rerun).
9. **When the release is correct, commit and publish it through the normal TDWG release process.** See [3.8](#38-commit-publish-and-test).

For draft work before ratification, use the same process in a fork or working branch; see [3.9](#39-generating-drafts).

# 3 Detailed workflow

## 3.1 Create the working branch and release directory

1. Clone the TDWG [`rs.tdwg.org`](https://github.com/tdwg/rs.tdwg.org) repository, or a fork if you do not have write access to the TDWG repository.
2. Create a working branch from the repository state that should immediately precede the release. A branch name such as `ac-changes-YYYY-MM-DD` or `dwc-changes-YYYY-MM-DD` is useful.
3. Create or update the release-specific revision directory under `process`. The normal pattern is a dated directory such as `dwc-revisions/dwc-revisions-YYYY-MM-DD`.
4. Preserve the source inputs and processor/configuration changes in Git. Making a commit before running `process.py` is RECOMMENDED because it clearly distinguishes the pre-processing release state from generated metadata, even though the processor no longer requires branch recreation between iterations.

The processor operates on the current working tree, so source/configuration edits do not have to be committed before processing. The checkpoint is for maintainability and review, not a technical requirement.

## 3.2 Prepare namespace release-input CSV files

Each configured namespace MUST have a release-input CSV in the configured release directory. The filename is the configured `pref_namespace_prefix` followed by `.csv`.

For an existing namespace:

- start from the column structure used by a recent release;
- retain the required headers;
- include a data row for each term that is new or whose metadata changes in this release; and
- use a header-only CSV when the namespace participates in the release but has no term changes.

When updating an existing term, reuse unchanged values from the authoritative current metadata where practical. This minimizes accidental lexical changes to fields that were not intended to change.

For a newly created Term List, set `new_term_list: true` for that namespace in `config.yaml`. For an existing Term List, set it to `false`. Preflight validation checks this declaration against existing repository Term List metadata and fails if the declaration and repository state disagree.

Borrowed namespaces and utility namespaces follow the configuration rules documented in `config.yaml`. Borrowed namespaces require an explicit `termlist_uri`; non-borrowed namespaces normally use the namespace IRI itself as the Term List IRI.

See [4.1](#41-terms-and-term-versions) and [4.2](#42-term-lists-and-term-list-versions) for the metadata affected by namespace processing.

## 3.3 Configure the complete release in `config.yaml`

`process/config.yaml` is the stable release declaration. It is not merely a list of resources that changed.

At the release level it supplies, among other settings:

- `date_issued`;
- `local_offset_from_utc`;
- the Standard IRI and applicable Standard metadata;
- `revision_directory` and, when supplied, `release_directory`;
- `decision_number` and `decisions_text`;
- the complete list of current Vocabularies; and
- the complete list of current direct Documents.

Each Vocabulary configuration supplies its identity and metadata, the IRI of its human-readable List-of-Terms Document, its vocabulary type, and its complete list of participating namespaces/Term Lists. Each namespace configuration supplies the namespace identity, dataset names, Term List identity and metadata, redirect construction information, and flags such as `borrowed`, `utility_namespace`, and `new_term_list`.

The `documents` array declares the current direct Document parts of the Standard. Do not limit this list to Documents changed in the release. Each Document entry contains its permanent Document IRI and its contributor declaration, may supply Document metadata that override release-level `document_defaults`, and, for non-List-of-Terms Documents, may contain the Boolean release-control flag `modified`.

`document_defaults` provides metadata shared across configured Documents. Supported Document metadata include the title, abstract, creator, media type, access URL, browser redirect URI, publisher, license statement, license URI, and comment. The processor rejects derived lifecycle or containment fields such as `current_iri`, `dcterms_isPartOf`, `doc_created`, `doc_modified`, and `citation` when they are supplied in a Document declaration because those values are derived from release state.

Each configured Document must resolve, after `document_defaults` and per-Document overrides are combined, to the complete required Document metadata expected by the processor. Contributor declarations are also centralized in `config.yaml` and supply the contributor identity/literal, role, role URI, affiliation, and affiliation URI used to maintain current and versioned author/role metadata.

A single processing run can contain multiple Vocabularies. Namespace prefixes and dataset names must be unambiguous across the complete release configuration.

`vocab.yaml` is **not used by the current processor**. Vocabulary and Standard release configuration that earlier workflows split between files is now represented in `config.yaml`.

Two consequences of this configuration model are particularly important:

1. The configured Vocabulary/namespace hierarchy is authoritative for **current Term List ownership**. A Term List can move from one Vocabulary to another without changing any of its terms.
2. The configured Vocabularies plus the `documents` list are authoritative for **current Standard composition**. A new Standard version is constructed from this current declaration, not by copying the parts of the preceding Standard version.

See [4.3](#43-vocabularies-and-vocabulary-version-snapshots) and [4.4](#44-standard-composition-and-standard-version-snapshots).

## 3.4 Prepare Document metadata

Document metadata and contributors are declared centrally in the release-level `documents` array in `process/config.yaml`. Common metadata may be supplied once in `document_defaults` and overridden where necessary in an individual Document declaration.

The permanent Document IRI is supplied by the `document` key. The processor derives rather than configures:

- `current_iri` from `document`;
- `dcterms_isPartOf` from the configured Standard;
- `doc_created` for a genuinely new Document from `date_issued`;
- `doc_modified` for a new or changed Document from `date_issued`; and
- the current citation from the resolved Document metadata and release date.

Maintainers therefore MUST NOT supply those derived fields in a Document declaration.

### Vocabulary-associated Lists-of-Terms Documents

The List-of-Terms Document identified by each Vocabulary's `list_of_terms_iri` is managed automatically as part of Vocabulary processing. Its Document declaration supplies the metadata and contributors used when a version is required, but it MUST NOT contain `modified`. A new List-of-Terms Document version is created when the associated Vocabulary release state requires the human-readable Document metadata to advance, for example because a member Term List changed or the Vocabulary's current Term List membership changed.

### Other configured Documents

For Documents that are not Vocabulary-associated Lists of Terms:

- a Document absent from current Document metadata is treated as new and receives its first version in the target release;
- an existing Document receives a new target-date version only when its declaration contains `modified: true`; and
- an existing Document without `modified: true` retains its latest applicable version.

The processor derives the target lifecycle dates from `date_issued`; maintainers do not enter `doc_modified` as a release-control field.

A same-release rerun does not create a duplicate Document version when the target-date version already exists.

### Delivery metadata

Document delivery metadata are reconciled independently of semantic Document versioning. Changes to `browserRedirectUri`, `accessUrl`, or media type may update the current Document delivery metadata and the latest applicable version's delivery/format metadata without requiring `modified: true` or creating a new Document version. This allows a Document to move to a different hosting or source location without asserting that its semantic content changed.

See [4.5](#45-document-metadata).

## 3.5 Run the processor

From the repository's `process` directory, preview the complete release before publishing:

```bash
python process.py --dry-run
```

If the preview is satisfactory, run the publishing mode:

```bash
python process.py
```

Both invocations execute the same release-processing logic in a staged repository. The outer invocation does not write release metadata directly into the working repository. In normal mode it:

1. copies the repository, excluding Git internals, Python caches, prior logs, and prior reports, to a temporary workspace;
2. runs the complete processor in that staged repository;
3. performs release preflight validation before release metadata is generated;
4. completes all processing in staging;
5. compares the staged repository with the state copied at the start of the run;
6. verifies that paths to be published were not changed concurrently in the real working tree;
7. publishes the staged metadata delta to the working repository; and
8. publishes the processing log and release report only after metadata publication succeeds.

If staged processing fails, no generated metadata from that run is published to the caller's working tree. If publication itself fails after some files have been replaced, the publication layer attempts to restore all affected paths to their pre-publication state.

### Dry-run preview

With `--dry-run`, the processor performs the same preflight and full staged processing as normal mode, including generation of the release report and processing log inside the temporary workspace. It then compares staged repository files with the initial staged snapshot and prints three path lists: `CREATED`, `MODIFIED`, and `DELETED`, each with a count. It also lists the staged report and log filenames. The staged report and log contents are **not retained**, and no repository metadata, log, or report is published. The temporary workspace is removed on exit.

The dry-run file comparison excludes `.git`, Python caches, and `process/logs` and `process/reports`. Consequently, the counts describe proposed changes to repository metadata and other tracked-scope files, **not** the number of generated log/report files. The printed `CREATED`/`MODIFIED`/`DELETED` lists are a preview of the transaction delta, not a substitute for inspecting the actual metadata content after a normal run.

A successful dry run reports `DRY RUN complete. Repository, logs, and reports unchanged.` A processing or preflight failure exits unsuccessfully without publishing staged output. Dry-run mode does not perform the normal publication step or its concurrent-edit check; if the working tree changes after the preview, repeat the preview before publishing.

Run `python process.py --help` to see the available command-line options.

### Preflight validation

Preflight checks include release/configuration structure, required namespace input CSVs, duplicate current identities, duplicate dated resource versions, ambiguous historical resource/date combinations, invalid historical dates, `new_term_list` consistency, and the existence/shape of metadata tables required for existing Term Lists. The intent is to reject histories that cannot be interpreted deterministically rather than resolving them by CSV row order or URI-string heuristics.

## 3.6 Review the generated release

A successful run is not the end of review. Inspect both the operational outputs and the repository diff.

Useful commands from the repository root are:

```bash
git diff --check
git status --short
git diff --stat
git diff
```

Also inspect:

- `process/reports/release-report-YYYY-MM-DD.md`;
- `process/logs/process-YYYY-MM-DD.log`; and
- the console summary produced during processing.

The log and report are operational review outputs rather than authoritative metadata. They are published after the metadata transaction succeeds and are normally excluded from the repository metadata transaction itself. A dry run prints the names of the staged log and report but does not retain them; run `python process.py` to publish those outputs for review.

For a substantive review, confirm that:

- only intended terms received new versions;
- each changed Term List has the intended complete target-date membership;
- current Term List-to-Vocabulary ownership matches `config.yaml`;
- each target Vocabulary snapshot contains the correct applicable Term List versions;
- current Standard composition matches the configured Vocabularies and Documents;
- the target Standard version contains the correct applicable versions of all configured parts;
- only Documents intended to change received target-date versions;
- configured namespace redirects match the intended human-readable destinations;
- the Executive Committee decision and affected-resource links are correct; and
- unchanged resources were not spuriously re-versioned.

Section [4](#4-what-processpy-modifies) identifies the principal metadata tables involved in these checks.

## 3.7 Correct and rerun

If the generated result is wrong because the source CSVs, `config.yaml` release declaration, centralized Document metadata/contributors, or persistent current-membership declarations are wrong, correct the authoritative input and run `process.py` again on the same working branch.

The processor is designed to be deterministic and same-release idempotent. In particular:

- an unchanged rerun should create no additional repository metadata changes;
- generated identities are reconciled rather than duplicated;
- current containment is reconciled from configuration; and
- target Vocabulary and Standard membership snapshots are reconstructed from current membership and applicable dated child versions.

Deleting and recreating a processing branch between iterations is therefore not part of the normal workflow.

For an explicit same-release idempotence check after successful normal processing, run:

```bash
python process.py --dry-run
```

The expected result is `CREATED (0)`, `MODIFIED (0)`, and `DELETED (0)`. This checks the staged repository delta without rewriting the published log and report. For deeper processor testing, a file-hash manifest of the processed repository (excluding `.git`, `__pycache__`, `process/logs`, and `process/reports`) can also be compared before and after a normal rerun.

## 3.8 Commit, publish, and test

When the generated metadata is satisfactory:

1. commit the release source inputs, configuration changes, and generated authoritative metadata;
2. submit or merge the branch according to the applicable TDWG maintenance and ratification procedure;
3. test machine-readable dereferencing through the TDWG test infrastructure when applicable; and
4. coordinate publication of the human-readable List-of-Terms or other standard documents so that term redirects resolve to valid fragment identifiers when the production release goes live.

For example, after merge, a changed term such as `http://rs.tdwg.org/eco/terms/protocolNames` can be checked through the corresponding `rs-test.tdwg.org` representation before production deployment. Deployment and front-end caching can introduce delays.

A repository release of `rs.tdwg.org` triggers production deployment according to the infrastructure release procedure.

## 3.9 Generating drafts

The same workflow can be used before ratification in a fork or draft branch. Draft processing is useful for proofreading metadata, generating candidate List-of-Terms documents, review by a Maintenance Group, and preparation for Executive Committee consideration.

The normal draft cycle is:

1. edit the release CSV/YAML inputs;
2. run `python process.py --dry-run` to validate the draft and preview the proposed metadata changes;
3. run `python process.py` when generated metadata and reports are needed for review or downstream draft document builds;
4. inspect the generated metadata and build downstream draft documents;
5. correct the inputs as necessary, preview again, and rerun on the same branch.

When the draft is finalized, preserve the release inputs in the normal review/ratification workflow. After ratification, ensure that `date_issued` is the actual release/ratification date and process the final release from the appropriate pre-release repository state.

## 3.10 New Term Lists and column-header mappings

When a new Term List is created, `process.py` creates its basic current-term and term-version dataset infrastructure from templates. The configured `vocab_type` selects the appropriate mapping template for simple vocabularies or controlled vocabularies.

If the release-input CSV contains additional property columns beyond those represented by the selected template, the generated column mapping file for the current-term dataset must be edited so that each source column maps to the intended RDF predicate and value type.

The mapping file is in the current-term dataset directory and normally ends in `-mappings.csv`. Its principal fields identify:

- the source column header;
- the predicate/CURIE;
- the value type (`iri`, `language`, `datatype`, or `plain`);
- an optional language or datatype attribute; and
- an optional fixed or prepended namespace value.

If a newly used namespace prefix is not already present in the dataset's `namespace.csv`, add it there as well.

For more background on the mapping format, see [guid-o-matic mapping documentation](https://github.com/baskaufs/guid-o-matic/blob/master/use.md#recording-the-column-mappings-from--the-metadata-table-to-rdf-triples).

## 3.11 Legacy notebooks and term deprecations

The Jupyter notebooks `simplified_process_rs_tdwg_org.ipynb` and `process_rs_tdwg_org.ipynb` record historical development of the processor. They are no longer the authoritative implementation and MUST NOT be substituted for the current `process.py` release workflow.

They may still be useful for understanding historical behavior, but the current processor has diverged substantially through release-level configuration, preflight validation, transaction handling, deterministic version selection, complete snapshot reconstruction, Document integration, redirect reconciliation, and same-release idempotence.

Term deprecation is not supported by the ordinary workflow described in this document. A proposed deprecation should be treated as an exceptional maintenance operation requiring explicit analysis of the affected current and historical metadata before changes are made. Do not assume that an old notebook can be run unchanged to perform a safe deprecation.

# 4 What `process.py` modifies

This section describes the principal metadata consequences of a successful release run. It is intended both as implementation documentation and as a review checklist.

## 4.1 Terms and term versions

For each namespace input row, the processor determines whether the term is new or modified relative to current and historical metadata.

For TDWG-minted, non-utility namespaces, a new or modified term receives a dated term-version record. For a modified term, the latest unambiguous version issued before the target release is selected as its predecessor and is marked superseded; the target-date version is recommended. Current term metadata is updated in place, while genuinely new terms are added to the current-term dataset.

Borrowed and utility namespaces do not use the same TDWG term-version mechanism. Their applicable current metadata are updated according to their configured processing mode.

The processor also maintains the current-term-to-version join metadata and applicable replacement relationships. Same-release reruns reconcile stable identities rather than appending duplicate versions or self-replacement assertions.

## 4.2 Term Lists and Term List versions

A Term List changes when it has term changes, is genuinely new, or its configured Term List-level metadata changes.

The processor maintains:

- `term-lists/term-lists.csv` for current Term List metadata;
- `term-lists/term-lists-members.csv` for current term membership;
- `term-lists/term-lists-versions.csv` for current-to-version joins;
- `term-lists-versions/term-lists-versions.csv` for dated Term List versions;
- `term-lists-versions/term-lists-versions-members.csv` for complete dated membership snapshots; and
- `term-lists-versions/term-lists-versions-replacements.csv` for version replacement relationships.

For an existing TDWG Term List, the new target-date membership snapshot starts from the latest predecessor membership and replaces the version of each modified term while adding versions of genuinely new terms. The processor validates that the predecessor contains at most one version for each term and that a term classified as new was not already present.

A header-only namespace CSV does not by itself create a new Term List version. However, a Term List can still receive a new version if its configured Term List-level metadata changes.

## 4.3 Vocabularies and Vocabulary-version snapshots

Current Term List membership in Vocabularies is maintained in:

`vocabularies/vocabularies-members.csv`

The configured Vocabulary/namespace hierarchy in `config.yaml` is authoritative for current ownership. During processing, a configured Term List is removed from any prior Vocabulary owner and associated with its configured Vocabulary. This allows containment changes even when the Term List itself has no term changes.

If a Vocabulary loses its Term Lists through such transfers and has no current Term List members remaining, it is treated as retired for version-status purposes: its existing versions through the target date are superseded, but the current Vocabulary identity and historical Vocabulary/version records are retained. No artificial target-date Vocabulary version is minted merely to express retirement.

When a target Vocabulary version is required, its membership is constructed as a **complete snapshot** of the Term Lists currently declared for that Vocabulary. Each current Term List identity is resolved to the applicable Term List version on the release date: a target-date version is used when one exists; otherwise the latest unambiguous earlier version is carried forward.

The relevant dated tables include:

- `vocabularies-versions/vocabularies-versions.csv`;
- `vocabularies-versions/vocabularies-versions-members.csv`; and
- `vocabularies-versions/vocabularies-versions-replacements.csv`.

Historical Vocabulary-version membership is not rewritten merely because current containment changes.

## 4.4 Standard composition and Standard-version snapshots

Current direct Standard composition is maintained in:

`standards/standards-parts.csv`

For the configured Standard, `process.py` reconciles this table to exactly the Vocabularies and Documents declared by the current `config.yaml`. Vocabulary parts are recorded as `tdwgutility:Vocabulary`; Document parts are recorded as `foaf:Document`.

The target Standard-version snapshot is maintained in:

`standards-versions/standards-versions-parts.csv`

Each configured Vocabulary and Document is resolved to the latest applicable version on or before the target release date. A target-date version is used when it exists; otherwise the latest unambiguous prior version is carried forward. The resulting rows are the complete composition snapshot of that Standard version.

Historical Standard-version snapshots remain historical evidence and are not rewritten simply because current composition changes.

Standard current/version metadata and replacement relationships are maintained in the corresponding `standards/` and `standards-versions/` tables.

## 4.5 Document metadata

Document metadata are maintained in the `docs/`, `docs-versions/`, and `docs-roles/` tables directly from the centralized release declaration in `config.yaml`.

The processor distinguishes **Document identity and lifecycle state**, **semantic versioning**, and **delivery metadata**:

- the permanent Document identity comes from the configured `document` IRI;
- Standard containment is derived from the configured Standard;
- creation and modification dates are derived from repository history and `date_issued`;
- non-List-of-Terms Documents receive a new version only when they are new or explicitly declared `modified: true`;
- Vocabulary-associated Lists-of-Terms Documents receive versions according to Vocabulary/Term List release state rather than a per-Document `modified` flag; and
- delivery metadata such as redirect URI, access URL, and media type can be reconciled without creating a semantic Document version.

For a changed existing Document, processing normally:

- creates or reconciles the target-date Document version;
- updates current Document metadata from the resolved release declaration;
- records current and target-version contributor/author information;
- records current and target-version format/access information;
- archives the immediately preceding version's redirect/access information when necessary; and
- records the target-version-to-predecessor replacement relationship.

For a genuinely new Document, the current Document and its first version are created. Its creation and modification dates are both the target release date.

For an unchanged existing Document, no semantic version is created merely because the Document remains a declared part of the Standard. The latest applicable version is carried into the target Standard-version snapshot by reference. Delivery metadata may nevertheless be reconciled independently.

The Document updater preserves stable row/scope ordering and stable identities on same-release reruns so that a semantically unchanged rerun is also byte-stable.

## 4.6 Human-readable term redirects

Current dereferencing rules for term and term-version datasets are maintained in:

`html/redirects.csv`

Redirect metadata is reconciled from each namespace's configuration **whether or not that namespace has term changes in the release**. This is important because redirect behavior is current infrastructure state, not a side effect of minting a new Term List version.

Vocabulary maintainers MUST ensure that the fragment identifiers generated in the human-readable List-of-Terms document follow the pattern declared by `prepend_url`, `use_namespace_in_fragment`, and `separator` in `config.yaml`.

For example, a Darwin Core redirect may map `http://rs.tdwg.org/dwc/terms/recordedBy` to `https://dwc.tdwg.org/list/#dwc_recordedBy`.

## 4.7 Executive Committee decision metadata

The release decision identity is derived from `date_issued` and `decision_number`. The processor maintains:

- `decisions/decisions.csv`; and
- `decisions/decisions-links.csv`.

A release decision is added once and reused on same-release reruns if its configured metadata agrees. Changed term IRIs are linked to the decision as affected resources, and duplicate relationship rows are suppressed.

## 4.8 Version status and dataset-index metadata

After resource-level processing, version statuses are reconciled from resource identity and release chronology. This ensures that same-release reruns reconstruct the intended recommended/superseded state rather than depending on incidental starting status.

The processor also updates `index/index-datasets.csv` modification metadata for metadata datasets actually affected at the corresponding resource level.

## 4.9 Processing log and release report

A successful run writes:

- `process/logs/process-YYYY-MM-DD.log`; and
- `process/reports/release-report-YYYY-MM-DD.md`.

These are generated in staging and published only after the metadata transaction succeeds in normal mode. In dry-run mode they are generated only within the temporary workspace; their filenames are reported, but the files are not retained. The log records namespace-level actions and created/modified files. The release report summarizes the resulting configured Standard, its Vocabulary and Term List release composition, and release-input term-change counts. It is suitable as a review aid or starting point for a GitHub Release description.

Neither replaces review of the authoritative repository diff.

# 5 Building a human-readable List of Terms document

`process.py` updates the authoritative metadata and the metadata record for a Vocabulary-associated List-of-Terms Document, but it does not build the human-readable List-of-Terms content itself. That build remains a Maintenance Group responsibility.

The build process SHOULD use authoritative current metadata from `rs.tdwg.org` together with the applicable centrally declared Document metadata so that human-readable and machine-readable representations remain consistent.

The Darwin Core and Audiovisual Core build systems have evolved substantially from the older example notebooks in this repository and support translation workflows. A Maintenance Group creating or modernizing a build system should therefore use a currently maintained standard build as its starting point rather than assume that historical `page_build_scripts` examples represent current best practice.

A List-of-Terms build commonly combines:

- hand-maintained introductory/document text;
- authoritative current term metadata for one or more Term Lists;
- Document metadata; and
- standard-specific organization rules such as grouping properties under display categories.

Where `tdwgutility:organizedInClass` is used for presentation grouping, it is an organizational relationship and does not imply an RDF domain declaration for the grouped property.

# 6 Generating JSON-LD for controlled vocabularies

Generation of multilingual JSON-LD for controlled vocabularies is ancillary to the `rs.tdwg.org` release processor. Translation workflows for actively maintained standards may instead be integrated with systems such as CrowdIn and standard-specific build pipelines.

Historical tooling for JSON-LD generation remains under `cv_json_ld`, but maintainers should verify that it is still appropriate for the standard and translation workflow before relying on it for a new release.

# 7 Reference

## 7.1 Standards hierarchy

The TDWG metadata model organizes relevant resources at the levels of Standards, Vocabularies, Term Lists, Terms, and their dated versions.

![TDWG metadata model](https://raw.githubusercontent.com/tdwg/vocab/master/tdwg-standards-hierarchy-2017-01-23.png)

A change at a lower level can require a new version at higher levels. However, the current processor distinguishes **resource change** from **containment change**. A Vocabulary or Standard version can be required because its membership/composition changed even when no child term metadata changed.

## 7.2 Current membership versus dated snapshots

The metadata distinguishes between current containment declarations and dated historical snapshots.

Current tables answer questions such as:

- Which terms are currently in this Term List?
- Which Term Lists currently belong to this Vocabulary?
- Which Vocabularies and Documents currently belong directly to this Standard?

Dated membership tables answer a different question: what was the complete membership of a particular dated resource version?

For Vocabularies and Standards, the current containment declarations are authoritative inputs to the next release. Historical membership snapshots are preserved but are not copied forward as the source of current membership.

## 7.3 Applicable version selection

When constructing a dated parent snapshot, the processor resolves each declared current child identity to one applicable dated version:

- if exactly one version exists on the target release date, that version is used;
- otherwise the latest unambiguous version issued before the target date is carried forward.

Ambiguous duplicate identities or duplicate versions for the same resource/date are errors. The processor does not resolve ambiguity by row order.

For modified terms, predecessor selection follows the same chronology principle: the latest version issued strictly before the target release is the predecessor.

## 7.4 Determinism and same-release idempotence

Release metadata timestamps generated by the processor are derived deterministically from the release date and configured UTC offset rather than the wall-clock time at which the script happens to run.

Stable resource identities and relationship rows are reconciled so that a same-release rerun does not append duplicate versions, memberships, replacement assertions, decision links, or Document metadata scopes. After processing a release, `python process.py --dry-run` provides a direct check of this property by reporting whether the same inputs would produce any further file changes.

The intended invariant is:

> Given the same repository state and release inputs, processing the same release again produces no repository metadata changes.

This property makes source correction and rerunning on the same branch a supported maintenance workflow rather than requiring reconstruction from a pre-processing branch after every iteration.
