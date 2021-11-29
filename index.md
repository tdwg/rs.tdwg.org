# TDWG Standards Metadata HTML landing page

This site serves primarily as a means to serve TDWG metadata using the correct `Content-Type` headers. Raw data served directly from GitHub always is sent with a `text/plain` content type. This minimal site (using GitHub Pages) serves files using a content type based on the file extension.

For the main landing page, see the repository readme visible at the [repository landing page](https://github.com/tdwg/rs.tdwg.org).

## Some links

Multilingual `establishmentMeans` controlled vocabulary demo page (still need to fix page to acknowledge translators):
- [English](cvJson/display-cv.html?en)
- [Dutch](cvJson/display-cv.html?nl)
- [Spanish](cvJson/display-cv.html?es)
- [French](cvJson/display-cv.html?fr)
- [Russian](cvJson/display-cv.html?ru)
- [Chinese (Traditional)](cvJson/display-cv.html?zh-Hant) - labels only, needs definition translations

[multilingual field labels (JSON)](cvJson/field_labels.json)

The following JSON files still need to be modified to include translator metadata:

### Darwin Core controlled vocabularies:

| controlled vocabulary | format | extension | media type | languages |
|---------------------- | ------ | --------- | ---------- | --------- |
| degreeOfEstablishment | [JSON-LD](cvJson/degreeOfEstablishment.json) | json | application/json | en, de, es, fr, ko (incomplete) |
| degreeOfEstablishment | [JSON-LD](cvJson/degreeOfEstablishment.jsonld) | jsonld | application/ld+json | en, de, es, fr, ko (incomplete) |
| degreeOfEstablishment (standard metadata) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/degreeOfEstablishment/degreeOfEstablishment.csv) | csv | text/plain | en |
| degreeOfEstablishment (translations) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/degreeOfEstablishment/degreeOfEstablishment-translations.csv) | csv | text/plain | en, de, es, fr, ko (incomplete) |
| establishmentMeans | [JSON-LD](cvJson/establishmentMeans.json) | json | application/json | en, es, nl, fr, ru, zh-Hant (labels only) |
| establishmentMeans | [JSON-LD](cvJson/establishmentMeans.jsonld) | jsonld | application/ld+json | en, es, nl, fr, ru, zh-Hant (labels only) |
| establishmentMeans (standard metadata) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/establishmentMeans/establishmentMeans.csv) | csv | text/plain | en |
| establishmentMeans (translations) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/establishmentMeans/establishmentMeans-translations.csv) | csv | text/plain | en, es, nl, fr, ru, zh-Hant (labels only) |
| pathway | [JSON-LD](cvJson/pathway.json) | json | application/json | en, es, fr (incomplete definitions), ko (incomplete), nl (incomplete definitions) |
| pathway | [JSON-LD](cvJson/pathway.jsonld) | jsonld | application/ld+json | en, es, fr (incomplete definitions), ko (incomplete), nl (incomplete definitions) |
| pathway (standard metadata) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/pathway/pathway.csv) | csv | text/plain | en |
| pathway (translations) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/pathway/pathway-translations.csv) | csv | text/plain | en, es, fr (incomplete definitions), ko (incomplete), nl (incomplete definitions) |

### Audubon Core controlled vocabularies

| controlled vocabulary | format | extension | media type |
|---------------------- | ------ | --------- | ---------- |
| format | [JSON-LD](cvJson/format.json) | json | application/json | en, de, fr (labels only), ko (incomplete), nl, zh-Hant (incomplete) |
| format | [JSON-LD](cvJson/format.jsonld) | jsonld | application/ld+json | en, de, fr (labels only), ko (incomplete), nl, zh-Hant (incomplete) |
| format (standard metadata) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/format/format.csv) | csv | text/plain | en |
| format (translations) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/format/format-translations.csv) | csv | text/plain | en, de, fr (labels only), ko (incomplete), nl, zh-Hant (incomplete) |
| subtype | [JSON-LD](cvJson/acsubtype.json) | json | application/json | en, ru, zh-Hant (labels only) |
| subtype | [JSON-LD](cvJson/acsubtype.jsonld) | jsonld | application/ld+json | en, ru, zh-Hant (labels only) |
| subtype (standard metadata) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/acsubtype/acsubtype.csv) | csv | text/plain | en |
| subtype (translations) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/acsubtype/acsubtype-translations.csv) | csv | text/plain | en, ru, zh-Hant (labels only) |
| variant | [JSON-LD](cvJson/acvariant.json) | json | application/json | en, ru, zh-Hant (labels only) |
| variant | [JSON-LD](cvJson/acvariant.jsonld) | jsonld | application/ld+json | en, ru, zh-Hant (labels only) |
| variant (standard metadata) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/acvariant/acvariant.csv) | csv | text/plain | en |
| variant (translations) | [CSV](https://github.com/tdwg/rs.tdwg.org/raw/master/acvariant/acvariant-translations.csv) | csv | text/plain | en, ru, zh-Hant (labels only) |
