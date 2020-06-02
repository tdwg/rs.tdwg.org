# Creating a vocabulary spreadsheet

**Title:** Creating a vocabulary spreadsheet

**Date Mofified:** 2020-06-01

**Part of TDWG Standard:** Not part of any standard

**Abstract:** Vocabulary developers can specify the necessary metadata about terms that they are minting or borrowing using a simple CSV spreadsheet. This document provides information about how to prepare a spreadsheet during the vocabulary development phase.

**Contributors:** Steve Baskauf (TDWG Technical Architecture Group, TDWG Audubon Core Maintenance Group, TDWG Darwin Core Maintenance Group)

# Table of Contents

[1 Introduction](#introduction)

[2 Terminology](#terminology)

[3 Examples and details](#examples-and-details)

# 1 Introduction

The [TDWG Standards Documentation Specification](http://rs.tdwg.org/sds/doc/specification/) (SDS) prescribes how the metadata for vocabulary terms should be presented in  human- and machine-readable forms. However, it isn't necessary for vocabulary developers to understand the technical details of that specification in order to do their work. There are only a few key details that vocabulary creators need to understand in order to provide the information needed to generate the SDS-compliant documents. 

There are several key ideas that need to be understood prior to creating the spreadsheet. They will be explained in the following section. The last section of the document will provide details and examples for several categories of vocabulary terms.

# 2 Terminology

## 2.1 Terms related to vocabularies

**Term** A term is the main component of a vocabulary. Types of terms are: *properties* used to describe resources, *classes* used to categorize resources, and *controlled vocabulary terms* used as values of properties. Terms have human readable labels, machine-readable IRI identifiers, definitions, and other descriptive metadata.

**Normative** Normative content is prescriptive and specifies what is required to comply with a standard. It cannot be changed without going through a formal process described by the [TDWG Vocabulary Maintenance Specificiation](http://rs.tdwg.org/vms/doc/specification/) (VMS). 

**Non-normative** Non-normative content may be part of a standard, but it is not as rigorously regulated as normative content. It may be desirable to avoid changing non-normative content, but it may be changed at the discretion of the relevant vocabulary maintenance group if its members feel that the change would be beneficial.

**Term list** A set of related terms sharing the same namespace identifier. Borrowed terms will be part of one or more term lists that are separate from the terms minted by TDWG.

## 2.2 Important terms related to vocabulary metadata

**Definition** The term definition is normative and is worded to precisely define the meaning of the term. If the term is minted by TDWG, vocabulary creators bear the responsibility of writing a concise and clear definition. If the term is borrowed from a non-TDWG vocabulary, the term definition as presented by TDWG will be the same as what is found in the defining vocabulary. Every term is required to have a definition.

**Usage guidelines** Usage guidelines are optional and are often not used if a term is defined by TDWG. They are often used with terms borrowed from other vocabularies because they specify how a borrowed term should be used in the context of the borrowing TDWG vocabulary. They can also be used to communicate expectations about how the term should be used beyond the definition. Usage guidelines are generally be declared to be normative since they are prescriptive. 

**Notes** Notes are optional and are non-normative. Notes provide information that might be helpful to understand how to use a term, but are not prescriptive. Notes may provide examples and references to other helpful resources.

**Label** A label is a human-readable name for the term. A label would be appropriate to present to a human user in a pick list. Terms are required to have an English label, but that label is not normative. Users should not be expected to understand the meaning of the term from its label without the definition, although a clear label can help prevent confusion among terms. It is desirable to have additional labels in languages other than English, but the creation and maintenance of those labels occurs outside of the standards process and generally will take place following the initial adoption of a vocabulary.

**Term local name** The local name is a string of characters that identies the term within the scope of a term list as described by [Best Practice Recipes for Publishing RDF Vocabularies](https://www.w3.org/TR/swbp-vocab-pub/#naming). A local name may be related to a human label or it may be opaque. Based on past TDWG precedent, property and class local names have been related to the human readable labels. In any case, users should not be expected to understand the meaning of a term from its local name -- they should consult the term definition. Vocabuary developers may suggest term local names, but the final decision on term local names will be made at the time of ratification. Term local names for properties should be in lower [camelCase](https://en.wikipedia.org/wiki/Camel_case) and term local names for classes should be in upper CamelCase. Examples will be given below.

## 2.3 Technical terms related to vocabulary metadata (optional reading)

The following information explains how the term local name is used to generate the IRI of the term. However, understanding these technical details is not necessary for vocabulary development. 

**Term IRI** The term IRI is a globally unique identifier in the form specified by [RFC 3987](https://tools.ietf.org/html/rfc3987). In most cases, "IRI" and "[URI](https://tools.ietf.org/html/rfc3986)" are interchangeable. IRIs can be written in their full or abbreviated forms. An example of a TDWG-minted IRI in its full form is `http://rs.tdwg.org/dwc/terms/recordedBy`. IRIs will be generated at the time when a vocabulary is ratified, so vocabulary developers do not need to worry about them.

**Namespace** A namespace is a string of characters that denotes a set of terms grouped and defined as a unit. Such a group of terms is called a *term list*. All TDWG-minted terms have namespaces that begin with `http://rs.tdwg.org/`. For example, the namespace for the term list of IRI-valued Darwin Core terms is `http://rs.tdwg.org/dwc/iri/`. TDWG namespaces will be assigned at the time when a vocabulary is ratified, and vocabulary developers do not need to worry about them.

**Term name** The term name is an abbreviated IRI (also known as a [compact URI](https://www.w3.org/TR/curie/) or CURIE) that is composed of an abbreviation for the first part of the IRI (the *namespace*), followed by a colon, then the local name.  **Term names are NOT human-readable term labels!** The abbreviation `dwc:` is used for the namespace `http://rs.tdwg.org/dwc/terms/`, so the term name (abbreviated IRI) for `http://rs.tdwg.org/dwc/terms/recordedBy` would be `dwc:recordedBy`. IRIs are fundamentally intended for machine use, and an abbreviated IRI is interchangeable with an unabbreviated IRI. That is, a script that can consume IRIs should be able to translate `dwc:recordedBy` to `http://rs.tdwg.org/dwc/terms/recordedBy` and vice-versa. Vocabulary developers may suggest namespace abbreviations that will be combined with local names to form the term name, but that is optional.

# 3 Examples and details

## 3.1 Simple example - TDWG minted vocabulary

In this example, every term has a definition. Terms generally don't have usage guidelines (although they could if necessary.) Notes provide examples and recommended values when appropriate. The term local names are in lower camelCase for properties and upper CamelCase for classes. There is not necessarily any particulary relationship between the human-readable labels and the term local names (although they are similar in this example - see additional examples below). There is currently no consensus within TDWG about capitalization of labels, but the chosen capitalization scheme should be used consistently. The value for type must be one of the following: `http://www.w3.org/1999/02/22-rdf-syntax-ns#Property` for properties, `http://www.w3.org/2000/01/rdf-schema#Class` for classes, or `http://www.w3.org/2004/02/skos/core#Concept` for controlled vocabulary terms. 

[Link to spreadsheet](example-spreadsheets/simple-vocabulary.csv)

| term_localName | label | definition | usage | notes | type |
| -------------- | ----- | ---------- | ----- | ----- | ---- | 
| county | County | The full, unabbreviated name of the next smaller administrative region than stateProvince (county, shire, department, etc.) in which the Location occurs. | | Examples: "Missoula", "Los Lagos", "Mataró" | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property |
| georeferenceProtocol | Georeference Protocol | A description or reference to the methods used to determine the spatial footprint, coordinates, and uncertainties |  | Examples: "Guide to Best Practices for Georeferencing. (Chapman and Wieczorek, eds. 2006). Global Biodiversity Information Facility.", "MaNIS/HerpNet/ORNIS Georeferencing Guidelines", "Georeferencing Quick Reference Guide | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | 
| Occurrence | Occurrence | An existence of an Organism (sensu http://rs.tdwg.org/dwc/terms/Organism) at a particular place at a particular time. | | Examples: A wolf pack on the shore of Kluane Lake in 1988. A virus in a plant leaf in a the New York Botanical Garden at 15:29 on 2014-10-23. A fungus in Central Park in the summer of 1929. | http://www.w3.org/2000/01/rdf-schema#Class | 


## 3.2 More complex example including borrowed terms and additional properties

This example has the same features as the previous example, but it also includes two additional properties beyond the basic properties (organizedInClass and repeatable) that provide information specifically desired for Audubon Core. At the bottom of the table, there are two additional term lists of terms borrowed from other namespaces. They are separated by a row containing a note explaining their source. Note that the definitions of the terms have been copied exactly from their source. The borrowed term local names are the retained as the same as in their original source, despite the fact that the xmp: terms do not follow the lower camelCase convention for properties in TDWG. Also notice that usage guidelines are more commonly used in the borrowed terms where there is no control over the term definitions.

[Link to spreadsheet](example-spreadsheets/complex-vocabulary.csv)

| term_localName | label | definition | usage | notes | type | tdwgutility_organizedInClass | tdwgutility_repeatable |
| -------------- | ----- | ---------- | ----- | ----- | ---- | --------------------------- | ---------------------------- |
| hashFunction | Hash Function | The cryptographic hash function used to compute the value given in the Hash Value. |  | Recommended values include MD5, SHA-1, SHA-224,SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256 | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | http://rs.tdwg.org/ac/terms/ServiceAccessPoint | No |
| fundingAttribution | Funding | Text description of organizations or individuals who funded the creation of the resource. |  |  | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | http://rs.tdwg.org/dwc/terms/attributes/Attribution | Yes |
| timeOfDay | Time of Day | Free text information beyond exact clock times. |  | Examples in English: afternoon, twilight. | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | http://purl.org/dc/terms/PeriodOfTime | No |
| ServiceAccessPoint | Service Access Point Class | A specific digital representation of a media resource. | This term serves as a type for values of the ac:hasServiceAccessPoint property. | For example, a Service Access Point may have a specific resolution, quality, or format. | http://www.w3.org/2000/01/rdf-schema#Class | http://rs.tdwg.org/ac/terms/ServiceAccessPoint |  |
| Dublin Core dc: terms | | | | | |
| language | Language | A language of the resource. | Language(s) of resource itself represented in the ISO639-2 three-letter language code. ISO639-1 two-letter codes are permitted but deprecated. | An image may contain language such as superimposed labels. If an image is of a natural scene or organism, without any language included, the resource is language-neutral (ISO code "zxx"). Resources with present but unknown language are to be coded as undetermined (ISO code "und"). Regional dialects or other special cases should conform to the ISO639-5 Alpha-3 Code for Language Families and Groups, http://id.loc.gov/vocabulary/iso639-5.html, where possible or the IETF Best Practices for Tags Identifying Languages, https://tools.ietf.org/html/rfc5646, where not. See also the entry for dcterms:language in the Audubon Core term list document and see the DCMI FAQ on DC and DCTERMS Namespaces, https://web.archive.org/web/20171126043657/https://github.com/dcmi/repository/blob/master/mediawiki_wiki/FAQ/DC_and_DCTERMS_Namespaces.md, for discussion of the rationale for terms in two namespaces. Normal practice is to use the same Label if both are provided. Labels have no effect on information discovery and are only suggestions. | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | http://rs.tdwg.org/dwc/terms/attributes/ContentCoverage | Yes |
| type | Type | The nature or genre of the resource. | The value of dc:type SHOULD be a term name of any term from the DCMI Type Vocabulary, https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-7 RECOMMENDED term names for media items are "Collection", "StillImage", "Sound", "MovingImage", "InteractiveResource", and "Text". A Collection MUST be given a value of "Collection". Following the DC recommendations at http://purl.org/dc/dcmitype/Text, images of text SHOULD be given a value of "Text" for dc:type. A value for at least one of dc:type and dcterms:type MUST be supplied in an Audubon Core record but when feasible, supplying both can make the metadata more widely useful. The values of dc:type and dcterms:type SHOULD designate the same type, but in case of ambiguity dcterms:type prevails. | If the resource is a Collection, this term does not identify what types of objects it may contain. See also the entry for dcterms:type in the Audubon Core term list document and see the DCMI FAQ on DC and DCTERMS Namespaces, https://web.archive.org/web/20171126043657/https://github.com/dcmi/repository/blob/master/mediawiki_wiki/FAQ/DC_and_DCTERMS_Namespaces.md, for discussion of the rationale for terms in two namespaces. Normal practice is to use the same Label if both are provided. Labels have no effect on information discovery and are only suggestions. | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | http://rs.tdwg.org/dwc/terms/attributes/Management | No |
| Adobe xmp: terms | | | | | |
| CreateDate | Original Date and Time | The date and time the resource was created. For a digital file, this need not match a file-system creation time.  For a freshly created resource, it should be close to that time, modulo the time taken to write the file.  Later file transfer, copying, and so on, can make the file-system time arbitrarily different. | The date of the creation of the original resource from which the digital media was derived or created. The date and time MUST comply with the World Wide Web Consortium (W3C) datetime practice, https://www.w3.org/TR/NOTE-datetime, which requires that date and time representation correspond to ISO 8601:1998, but with year fields always comprising 4 digits. This makes datetime records compliant with 8601:2004, https://www.iso.org/standard/40874.html. AC datetime values MAY also follow 8601:2004 for ranges by separating two IS0 8601 datetime fields by a solidus ("forward slash", '/'). | What constitutes "original" is determined by the metadata author. Example: Digitization of a photographic slide of a map would normally give the date at which the map was created; however a photographic work of art including the same map as its content may give the date of the original photographic exposure. Imprecise or unknown dates can be represented as ISO dates or ranges. Compare also Date and Time Digitized in the Resource Creation Vocabulary. See also the wikipedia IS0 8601 entry, https://en.wikipedia.org/wiki/ISO_8601, for further explanation and examples. | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | http://purl.org/dc/terms/PeriodOfTime | No |
 | MetadataDate | Metadata Date | The date and time that any metadata for this resource was last changed. It should be the same as or more recent than xmp:ModifyDate. | Point in time recording when the last modification to metadata (not necessarily the media object itself) occurred. The date and time MUST comply with the World Wide Web Consortium (W3C) datetime practice, https://www.w3.org/TR/NOTE-datetime, which requires that date and time representation correspond to ISO 8601:1998, but with year fields always comprising 4 digits. This makes datetime records compliant with 8601:2004, https://www.iso.org/standard/40874.html. AC datetime values MAY also follow 8601:2004 for ranges by separating two IS0 8601 datetime fields by a solidus ("forward slash", '/'). | This is not dcterms:modified, which refers to the resource itself rather than its metadata. See also the wikipedia IS0 8601 entry, https://en.wikipedia.org/wiki/ISO_8601, for further explanation and examples. | http://www.w3.org/1999/02/22-rdf-syntax-ns#Property | http://rs.tdwg.org/dwc/terms/attributes/Management | No |

## 3.3 Simple controlled vocabulary

Controlled vocabularies have an additional required property that is not found in other vocabularies: a `controlled value string`. The controlled value string is NOT the human readable label and it is NOT the term local name. It is the plain text string that spreadsheet users should provide in lieu of using the term IRI. It is desirable that the controlled value string not require additional disambiguation, so it is recommended that it have the following characteristics:

- no spaces
- only ASCII alphabetic letters (no diacritics, no punctuation)
- rule-based capitalization (such as lower camelCase)
- memorable form suitable for human users (vs. opaque random strings)

The controlled value may be similar to the English human-readable label, but based on the criteria listed above (e.g. no spaces), it will probably not be the same. Vocabulary creators should think carefully how they will prevent their community from confusing the controlled value strings with the English label and the term local name.

In the example below, the local name is an opaque string and therefore unlikely to be confused with either the label or controlled value string. The controlled value sting is in lower camelCase. It is composed of words related to the label, but is unlikely to be confused with the label because the label includes spaces and punctuation.

The type of controlled vocabulary terms should be `http://www.w3.org/2004/02/skos/core#Concept`.

[Link to spreadsheet](example-spreadsheets/simple-cv.csv)

| term_localName | label | controlled value string | definition | usage | notes | type |
| -------------- | ----- | ----------------------- | ---------- | ----- | ----- | ---- | 
| e001 | native (indigenous) | native | A taxon occurring within its natural range |  | What is considered native to an area varies with the biogeographic history of an area and the local interpretation of what is a "natural range". See also https://www.iucn.org/sites/dev/files/iucn-glossary-of-definitions_march2018_en.pdf | http://www.w3.org/2004/02/skos/core#Concept |
| e002 | native: reintroduced | nativeReintroduced | A taxon re-established by direct introduction by humans into an area which was once part of its natural range, but from where it had become extinct. |  | Where a taxon has become extirpated from an area where it had naturally occurred it may be returned to that area deliberately with the intension of re-establishing it. See also https://www.iucn.org/sites/dev/files/iucn-glossary-of-definitions_march2018_en.pdf | http://www.w3.org/2004/02/skos/core#Concept |
| e003 | introduced (alien, exotic, non-native, nonindigenous) | introduced | Establishment of a taxon by human agency into an area that is not part of its natural range |  | Organisms can be introduced to novel areas and habitats by human activity, either on purpose or by accident. Humans can also inadvertently create corridors that breakdown natural barriers to dispersal and allow organisms to spread beyond their natural range. See also https://www.iucn.org/sites/dev/files/iucn-glossary-of-definitions_march2018_en.pdf | http://www.w3.org/2004/02/skos/core#Concept |

## 3.4 Controlled vocabulary with broader hierarchy

Terms in a controlled vocabulary may be related to other controlled vocabulary terms through a *broader* relationship.<sup>1</sup> That implies that if the narrower concept applies, the broader concept does as well. This relationship can be indicated in the spreadsheet by including a skos_broader column in the spreadsheet. Placing the local name of the broader term in that column will create that relationship when the metadata are generated. The broader terms are described in the same way as the narrower ones and they can be used if the appropriate narrower concept cannot be determined.

[Link to spreadsheet](example-spreadsheets/cv-hierarchy.csv)

| term_localName | label | skos_broader | controlled value string | definition | usage | notes | type |
| -------------- | ----- | ------------ | ----------------------- | ---------- | ----- | ----- | ---- | 
| p001 | biological control | p045 | biologicalControl | An organism occuring in an area because it was introduced for the purpose of biological control of another organism. | | See also Harrower CA, Scalera R, Pagad S, Schönrogge K, Roy HE (2017) Guidance for interpretation of CBD categories on introduction pathways. Technical note prepared by IUCN for the European Commission. IUCN, 100 pp. | http://www.w3.org/2004/02/skos/core#Concept |
| p002 | erosion control | p045 | erosionControl | Introduced for the purpose of erosion control/dune stabilization (windbreaks, hedges, etc). | | Probably only applicable only to plants. See also Harrower CA, Scalera R, Pagad S, Schönrogge K, Roy HE (2017) Guidance for interpretation of CBD categories on introduction pathways. Technical note prepared by IUCN for the European Commission. IUCN, 100 pp. | http://www.w3.org/2004/02/skos/core#Concept |
| p009 | agriculture (including biofuel feedstocks) | p046 | agriculture | Generally a plant grown with then intension of harvesting. | | Probably only applicable only to plants. See also Harrower CA, Scalera R, Pagad S, Schönrogge K, Roy HE (2017) Guidance for interpretation of CBD categories on introduction pathways. Technical note prepared by IUCN for the European Commission. IUCN, 100 pp. | http://www.w3.org/2004/02/skos/core#Concept |
 | p010 | Aquaculture / mariculture | p046 | aquacultureMariculture | Similar to the terms agriculture and farmed animals, but this is specifically related to aquatic organisms. | | See also Harrower CA, Scalera R, Pagad S, Schönrogge K, Roy HE (2017) Guidance for interpretation of CBD categories on introduction pathways. Technical note prepared by IUCN for the European Commission. IUCN, 100 pp. | http://www.w3.org/2004/02/skos/core#Concept |
 | p045 | release in nature | p051 | releaseInNature | Organisms transported by humans with the intension of releasing them in a (semi)natural environment with the intension that they should live their without further human aid. | | See also Harrower CA, Scalera R, Pagad S, Schönrogge K, Roy HE (2017) Guidance for interpretation of CBD categories on introduction pathways. Technical note prepared by IUCN for the European Commission. IUCN, 100 pp. | http://www.w3.org/2004/02/skos/core#Concept |
 | p046 | escape from confinement | p051 | escapeFromConfinement | Organisms intentionally transported by humans and intended to be kept in captivity or cultivation, but having inadvertently escaped from human control. | | See also Harrower CA, Scalera R, Pagad S, Schönrogge K, Roy HE (2017) Guidance for interpretation of CBD categories on introduction pathways. Technical note prepared by IUCN for the European Commission. IUCN, 100 pp. | http://www.w3.org/2004/02/skos/core#Concept |
 | p051 | intentional |  | intentional | The organism was specific brought to new area with the intension of keeping them alive in the new region, irrespective of whether they were intended to be cultivated or released into the wild. | | See also Harrower CA, Scalera R, Pagad S, Schönrogge K, Roy HE (2017) Guidance for interpretation of CBD categories on introduction pathways. Technical note prepared by IUCN for the European Commission. IUCN, 100 pp. | http://www.w3.org/2004/02/skos/core#Concept |

<sup>1</sup> This is allowed as part of the basic term metadata by the SDS since it does not generate any machine-computable entailments. Implementers may choose whether or not to make use of this information. 