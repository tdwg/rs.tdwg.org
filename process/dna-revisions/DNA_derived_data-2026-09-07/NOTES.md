# DNA derived data term lists — deviations

Source files for four borrowed term lists recording the MIxS, MIQE, GBIF and GGBN terms
used by the GBIF DNA derived data extension. Term metadata was extracted from
`rs.gbif.org` `extension/gbif/1.0/dna_derived_data_2024-07-11.xml` and its sandbox
successor; from here on these lists are the source of truth and the extension is generated
from them.

Only the deliberate departures are recorded below. Everything else follows
`create-vocabulary.md` and `process-vocabulary.md`.

## `ggbn:ratioOfAbsorbance260_280` — definition departs from the source vocabulary

`create-vocabulary.md` §2.2 says a borrowed definition SHOULD match the defining
vocabulary. This one does not, deliberately. GBIF's copy of the GGBN schema
(`rs.gbif.org` `extension/ggbn/materialsample.xml`) describes it as a ratio "at 280 nm and
230 nm", which contradicts the term's own name and appears to be copy-pasted from
`ratioOfAbsorbance260_230`. This list carries the corrected "260 nm and 280 nm".

**Do not "correct" this back to match GGBN when regenerating.** The typo is still live in
`extension/ggbn/materialsample.xml` and should be fixed there separately. These definitions
were checked against GBIF's copy of the GGBN schema, not against `data.ggbn.org` itself.

## MIxS local names are opaque numbers

MIxS identifies terms by zero-padded numeric IRIs — `samp_name` is
`https://w3id.org/mixs/0001107` — so `term_localName` is `0001107`, not `samp_name`. This
is intentional, not a data error. The Darwin Core Archive column heading is carried
separately, in the `name` column of `rs.gbif.org` `scripts/xml/dna_derived_data_list.csv`.

## Examples are single backtick-wrapped strings, not lists

MIxS uses both `;` and `,` inside single values (`FWD:GTGCC…;REV:GGACT…`,
`kmer set 21,33,55,77,99,121`), so splitting on either would corrupt them. Fourteen
comma-separated enumerations remain candidates for manual splitting.

## Known gaps

- Labels for the 31 non-MIxS terms were written by hand from the term names. If MIQE or
  GGBN publish canonical labels, those should win.
- Saara Suominen's `contributor_iri` is blank. The source document gives her the same ORCID
  as Dmitry Schigel, which is an error there.
