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

These JSON files still need to be modified to include translator metadata:

[establishmentMeans JSON-LD metadata with .json extension](cvJson/establishmentMeans.json)

[establishmentMeans JSON-LD metadata with .jsonld extension](cvJson/establishmentMeans.jsonld)

[format JSON-LD metadata with .json extension](cvJson/format.json)

[format JSON-LD metadata with .jsonld extension](cvJson/format.jsonld)
