# TDWG Standards Metadata HTML landing page

This site serves primarily as a means to serve TDWG JSON-LD metadata using the correct `Content-Type` headers. Raw data served directly from GitHub always is sent with a `text/plain` content type. This minimal site (using GitHub Pages) serves files using a content type based on the file extension.

For the main landing page, see the repository readme visible at the [repository landing page](https://github.com/tdwg/rs.tdwg.org).

## Multilingual translations

Multilingual `establishmentMeans` controlled vocabulary demo page (still need to fix page to acknowledge translators):
- [English](cvJson/display-cv.html?en)
- [Dutch](cvJson/display-cv.html?nl)
- [Spanish](cvJson/display-cv.html?es)
- [French](cvJson/display-cv.html?fr)
- [Russian](cvJson/display-cv.html?ru)
- [Chinese (Traditional)](cvJson/display-cv.html?zh-Hant) - labels only, needs definition translations

### Field labels

These [multilingual field labels (JSON)](cvJson/field_labels.json) can be used along with the label and definition translations to construct multilingual tools like the one above.

### Darwin Core controlled vocabularies:

The following JSON files still need to be modified to include translator metadata:

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


### Translators acknowledgements

Carla Novoa Sepúlveda, Staatliche Naturwissenschaftliche Sammlungen Bayerns - Botanische Staatssammlung München (SNSB-BSM; Bavarian Natural History Collections - Botanical State Collection Munich), https://orcid.org/0000-0001-6113-9725, español (Spanish): Audubon Core subtype, Darwin Core degreeOfEstablishment, Darwin Core establishmentMeans, Darwin Core pathway

Julie Dionne Lavoie, Observatoire Global du Saint-Laurent, français (French): Audubon Core subtype

Нина В. Филиппова (Nina V. Filippova), Югорский государственный университет (Yugra State University), https://orcid.org/0000-0002-9506-0991, Русский (Russian): Audubon Core subtype, Audubon Core variant, Darwin Core establishmentMeans

柯智仁 (Chihjen Ko), https://orcid.org/0000-0001-5912-1761, 繁體中文 (Chinese - traditional): Audubon Core subtype, Audubon Core variant, Darwin Core establishmentMeans, Audubon Core format

Mareike Petersen, https://orcid.org/0000-0001-8666-1931, Deutsch (German): Darwin Core degreeOfEstablishment, Audubon Core format

វេស្សន្តរទេស អ៊ឹង (Visotheary Ung), ISYEB (CNRS-MNHN), https://orcid.org/0000-0002-4049-0820, français (French): Darwin Core degreeOfEstablishment, Darwin Core establishmentMeans

Julie Dionne Lavoie, Observatoire Global du Saint-Laurent, français (French): Darwin Core degreeOfEstablishment, Darwin Core establishmentMeans, Darwin Core pathway

Francis Y, 한국인 (Korean): Darwin Core degreeOfEstablishment

William Ulate Rodriguez, Missouri Botanical Garden, St. Louis, Missouri, USA, https://orcid.org/0000-0003-2863-2491, español (Spanish): Darwin Core establishmentMeans

Sophie Pamerlon, GBIF France, https://orcid.org/0000-0003-4736-7419, français (French): Darwin Core establishmentMeans, Audubon Core format

Maxime Coupremanne, Belgian Biodiversity Platform, https://orcid.org/0000-0002-9052-9500, français (French): Darwin Core establishmentMeans, Darwin Core pathway

Braun Paul, Musée national d'histoire naturelle, Luxembourg, https://orcid.org/0000-0002-3620-6188, Deutsch (German): Audubon Core format

Anke Penzlin, Senckenberg, Deutsch (German): Audubon Core format

김목영 (Mokyoung Kim), 국립생태원 (National Institute of Ecology), 한국인 (Korean): Audubon Core format, Darwin Core pathway

Jorrit H. Poelen, Ronin Institute, https://orcid.org/0000-0003-3138-4118, Nederlands (Dutch): Audubon Core format

Paula F Zermoglio, IEGEBA-CONICET (Argentina), https://orcid.org/0000-0002-6056-5084, español (Spanish): Darwin Core pathway, Darwin Core establishmentMeans

Elie Tobi, Smithsonian Conservation Biology Institute, Gabon Biodiversity Program, https://orcid.org/0000-0002-6199-290X, français (French): Darwin Core pathway

Greg Jongsma, Florida Museum of Natural History, https://orcid.org/0000-0001-8790-2610, français (French): Darwin Core pathway

Tim Claerhout, Ghent University, https://orcid.org/0000-0002-1519-4536, Nederlands (Dutch): Darwin Core pathway

Sofie Meeus, Plantentuin Meise (Meise Botanic Garden), https://orcid.org/0000-0003-0715-8647, Nederlands (Dutch): Darwin Core estlishmentMeans

-------
Last modified 2021-11-29
