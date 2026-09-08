# DNA derived data term lists — deviations and review notes

Source files for the four borrowed term lists used by the GBIF DNA derived data
extension (`mixs-for-dna`, `miqe-for-dna`, `gbif-for-dna`, `ggbn-for-dna`).

The term metadata was extracted from the hand-maintained extension these lists replace as
the source of truth. Its provenance:

- `rs.gbif.org` `extension/gbif/1.0/dna_derived_data_2024-07-11.xml` — the last published
  release, and the last version maintained entirely by hand.
- `rs.gbif.org` `sandbox/extension/gbif/1.0/dna_derived_data_2026-04-14.xml` — a sandbox
  draft over that: typo fixes in two term names and one description, a usage comment split
  out of one definition, and `url` renamed to `associated_resource`.
- Five further MIxS v7 term renames applied on top of the sandbox draft
  (`estimated_size` → `estimated_genome_size`, `single_cell_lysis_appr` →
  `sc_lysis_approach`, `single_cell_lysis_prot` → `sc_lysis_method`, `_16s_recover` →
  `x16s_recover`, `_16s_recover_software` → `x16s_recover_software`).

From that point the term lists in this directory are the source of truth, and
`sandbox/extension/gbif/1.0/dna_derived_data_2026-09-07.xml` is *generated* from them by
`rs.gbif.org` `scripts/build-xml.py` — do not treat it as an input.

Everything below is a deliberate departure from the documented process or from a source
vocabulary. Each needs a reviewer's agreement before this is proposed upstream.

## 1. `ggbn:ratioOfAbsorbance260_280` — definition corrected, deviates from source

`create-vocabulary.md` §2.2 says a borrowed term's definition SHOULD match the defining
vocabulary. This one does not, deliberately.

GBIF's copy of the GGBN schema (`rs.gbif.org` `extension/ggbn/materialsample.xml`) reads:

> Ratio of absorbance at **280 nm and 230 nm** assessing DNA purity …

That contradicts the term's own name: a term called `ratioOfAbsorbance260_280` cannot be
a 280/230 ratio. The wording appears to have been copy-pasted from the sibling term
`ratioOfAbsorbance260_230` and never adjusted. This term list carries the corrected text:

> Ratio of absorbance at **260 nm and 280 nm** assessing DNA purity …

Decision: keep the correction rather than propagate a known error into TDWG metadata.

Two follow-ups:
- The typo is still live in `rs.gbif.org` `extension/ggbn/materialsample.xml` and should be
  fixed there separately.
- These definitions were checked against GBIF's copy of the GGBN schema, **not** against
  `data.ggbn.org` itself. Someone should confirm the authoritative GGBN wording. The other
  four GGBN definitions are byte-identical to GBIF's copy and need no attention.

## 2. `mixs-for-dna` — numeric term local names, and the upstream fix they depend on

MIxS identifies its terms with opaque zero-padded numeric IRIs: `samp_name` is
`https://w3id.org/mixs/0001107`. Per `create-vocabulary.md` §2.3 the local name is what
composes the term IRI, so `term_localName` here is `0001107`, not `samp_name`. All 91 MIxS
local names are 7-digit strings and the composed IRIs match MIxS's declared `slot_uri`
values exactly.

The Darwin Core Archive column heading is a separate concern and is supplied by the
optional `name` column of `rs.gbif.org` `scripts/xml/dna_derived_data_list.csv`. 92 rows
use it: the 91 MIxS terms, plus `gbif:dna_sequence`, whose IRI is lowercase while its
column heading is `DNA_sequence`.

### Background: this needed a fix to `dwcterms.py` upstream (merged)

`process.py` in this repository handles numeric local names correctly — it reads term data
through its own `readCsv()`, which uses the stdlib `csv` module and yields strings.

`dwcterms.py` in `tdwg/dwc` (`build/dwcterms.py`), which `rs.gbif.org` uses to build the
extension, did not. It read the term lists with `pd.read_csv(..., keep_default_na=False)`
and no `dtype`, so a column of nothing but digits was inferred as `int64` — `'0001107'`
became `1107`, losing the leading zeros before anything else ran, then failing outright on
the `term_iri` string concatenation with:

    UFuncTypeError: ufunc 'add' did not contain a loop with signature matching
    types (dtype('<U22'), dtype('int64'))

The fix adds `dtype=str` to all three reads in `create_metadata_table()` (current terms,
versions, translations). All three are required: `term_localName` is the merge key joining
them, and is used with the `.str` accessor when sorting, so the dtype must be consistent
across all three or the merge raises.

That fix was merged as **https://github.com/tdwg/dwc/pull/1058**, so nothing here is
blocked. `rs.gbif.org` re-downloads `dwcterms.py` from `tdwg/dwc` master on every
`update-translations.sh` run and picks it up automatically. Recorded here because it
explains why `term_localName` is numeric, and because anyone building against a
`dwcterms.py` predating that merge will hit the `UFuncTypeError` above.

No existing TDWG term list uses purely numeric local names — checked across every term list
in this repository — which is why this had not surfaced before. It is a latent bug for any
borrowed vocabulary with opaque numeric identifiers, not a MIxS-specific problem. Verified
against today's data: of the 191 CSVs the consumers read, only `term_deprecated` (bool) and
`tdwgutility_layer` (int64) change dtype under the fix, neither changes behaviour, and both
`build-csv_derivatives.py` and `build-webpages.py` produce byte-identical output.

## 3. Definitions and usage guidelines

Per `create-vocabulary.md` §2.2 and §3.2, borrowed definitions are the source vocabulary's
own and the borrowing vocabulary's wording goes in usage guidelines:

- **MIxS (91 terms)** — `rdfs_comment` is MIxS v7.0.1's `description` verbatim; verified
  identical for all 91. GBIF's biodiversity-audience rewrite moved to
  `dcterms_description`, populated on 19 terms.
- **GBIF / MIQE (26 terms)** — GBIF mints these, so GBIF's own text is the definition.
- **GGBN (5 terms)** — GGBN's definitions, subject to item 1 above.

## 4. Labels for the 31 non-MIxS terms

MIxS supplies `title` for its own terms. The GBIF, MIQE and GGBN labels were written by
hand from the term names (e.g. `pcr_primer_lod` → "PCR Primer Limit Of Detection"). If
MIQE or GGBN publish canonical labels, those should win.

## 5. Examples are single backticked strings, not lists

TDWG convention separates multiple examples with `` `a`; `b` ``. MIxS uses both `;` and `,`
*inside* single values (`FWD:GTGCC…;REV:GGACT…`, `kmer set 21,33,55,77,99,121`), so
splitting on either would corrupt them. Each example is therefore wrapped whole. Fourteen
comma-separated enumerations (`pathogenicity`, `target_gene`, …) are genuine candidates for
manual splitting later.

## 6. Not yet settled

- **Document IRI** `http://rs.tdwg.org/dwc/doc/dna/` is unverified against the
  standards-document IRI patterns (`process-vocabulary.md` step 8). Getting it wrong breaks
  dereferencing after ratification — confirm with the Maintenance Group or TAG.
- **`date_issued: 2026-09-07`** is not a ratification date. It must be set to the real one
  before the changes go live.
- **Saara Suominen's ORCID** is blank in `dwc_doc_dna/authors_configuration.yaml`. The
  source document gives her the same ORCID as Dmitry Schigel, which is an error there.
- **Governance.** These lists are recorded under Darwin Core (standard 450) with
  `borrowed: true`, so no term versions are minted and no authority is claimed over MIxS,
  GGBN or MIQE terms. Whether the DNA derived data extension belongs under Darwin Core or
  warrants its own vocabulary is a question for the Maintenance Group. See section 7 for
  what running the script actually asserts.

## 7. What running `process.py` asserts — read before merging derived data

Running the script does not just build term lists. It writes records that, taken at face
value, claim things that have not happened. None of this is wrong for a draft; all of it
is wrong if the derived data reaches master before ratification.

**A ratification decision is minted, unconditionally.** Every run appends a row to
`../decisions/decisions.csv`. There is no flag to suppress it. This run produced:

    term_localName : decision-2026-09-07_62
    label          : TDWG Executive Committee decision 62
    rdfs_comment   : Term lists recording the MIxS, MIQE, GBIF and GGBN terms used by
                     the GBIF DNA derived data extension. ...

Only `rdfs_comment` comes from this directory's `config.yaml` (`decisions_text`). The
label is a hardcoded string in `process.py` (line 1371) and the number is auto-incremented
from the last row's label — the previous entry is `decision-2026-05-26_61`, the
Establishment Means CV update. So the file now records an Executive Committee decision that
the Executive Committee has not made. A matching `decision_localName` is written against
all 122 term IRIs in `../decisions/decisions-links.csv`.

**A new version of the whole Darwin Core standard is minted.** `standards-versions.csv`
gains `http://www.tdwg.org/standards/450/version/2026-09-07` as `recommended` and marks
`.../version/2026-05-26` as `superseded`. The same happens to the vocabulary in
`vocabularies-versions.csv`. This is the entire standard, not just these four term lists.

**Redirects point at a page that does not list these terms.** `../html/redirects.csv` sends
all four lists to `https://dwc.tdwg.org/list/#`, the Darwin Core List of Terms. Until a
List of Terms document exists that includes them, term IRI dereferencing will land on a
page where they do not appear.

### Consequences

`date_issued` in `config.yaml` is currently `2026-09-07`, which is not a ratification date.
When the changes are actually ratified, that value must be set to the real date and the
derived data regenerated from scratch — the decision number will likely no longer be 62,
because other standards may consume numbers in the meantime.

This is why `process-vocabulary.md` §2.3 keeps derived data on a disposable branch: steps
1-10 put source in place and are committed, steps 11-17 generate derived data on a branch
made from it. Delete the branch, fix the source, branch again. Only the source branch
should be proposed upstream (step 17); rs.tdwg.org maintainers re-run steps 11-16
themselves after ratification.

**Do not merge the derived branch to master.**
