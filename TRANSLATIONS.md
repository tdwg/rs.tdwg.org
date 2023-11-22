# rs.tdwg.org translations

We are using [CrowdIn](https://crowdin.com/project/darwin-core) to translate Darwin Core and related terms into several languages.  CrowdIn tracks changes are made to the source text, and suggests identical or near-identical translations from other sources such as the GBIF.org website  (GBIF also use CrowdIn).

**If you wish to contribute, you *must* do this using CrowdIn — changes made directly in Git/GitHub will either be overwritten, or will interfere with the process used by CrowdIn.**

The resulting translations are in files named `*-translations.csv`, for example for [degreeOfEstablishment](./degreeOfEstablishment/degreeOfEstablishment-translations.csv).

## Technical process

Two Git branches are used by the process.

A branch "translations" stores source (English) files for translation, in a format suitable for Crowdin: one word or phrase per line, consistent column ordering and a stable identifier column ([example, degreeOfEstablishment.en.csv](https://github.com/tdwg/rs.tdwg.org/blob/translations/degreeOfEstablishment/degreeOfEstablishment.en.csv)).  It also stores the resulting translations in a similar format ([example, degreeOfEstablishment.es.csv](https://github.com/tdwg/rs.tdwg.org/blob/translations/degreeOfEstablishment/degreeOfEstablishment.es.csv)).

An interim branch, "crowdin_translations", is updated by CrowdIn soon after changes are made at https://crowdin.com/project/darwin-core.

[A script](https://github.com/tdwg/rs.tdwg.org/blob/translations/process/translations/build-translations.py) running on GBIF's [Jenkins server](https://builds.gbif.org/job/rs.tdwg.org-translations/) is triggered by GitHub when changes are made.  It

1. Merges any new or updated translations from the "crowdin_translations" branch to the "translations" branch.

2. Merges any changes from the "master" branch into the "translations" branch.

3. Updates the `*.en.csv` which are read by CrowdIn, if the terms or definitions have changes.

4. Updates the `*-translations.csv` files on the "master" branch with any new or changed translations.


