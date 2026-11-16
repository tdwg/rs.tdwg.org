# TDWG Standards Metadata

This repository contains the raw metadata about TDWG standards in CSV format. For a full explanation about how to access these data in various representations, visit <http://rs.tdwg.org/index>.

## IRIs: `http` or `https`

TDWG IRIs are served under `rs.tdwg.org` with either scheme, and the canonical scheme is chosen per vocabulary: the existing TDWG vocabularies use `http://rs.tdwg.org/…`, and a new vocabulary may use `https://rs.tdwg.org/…`. The tables record each resource's IRI with its own scheme, and a request under either scheme returns the resource described by that IRI. See [`process/process-vocabulary.md`](process/process-vocabulary.md), "Protocol (`http` or `https`)"; `index/dereferencing-test.py` checks that each vocabulary's RDF uses its own scheme.

## Biodiversity Data Quality (BDQ)

The BDQ standard's vocabularies and documents are processed on the `bdq-source` (inputs) and `bdq` (processed, deployed) branches for its public review, served at <https://bdq-public-review.rs.tdwg.org/> (tdwg/bdq#340); they use `https` IRIs. Their release inputs and BDQ-specific scripts are in [`process/bdq-revisions/`](process/bdq-revisions/README.md), and the generated ontology is described in [`process/process-ontology.md`](process/process-ontology.md).
