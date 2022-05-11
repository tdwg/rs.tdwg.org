# Latimer Core List of Terms

**Title**
: Latimer Core List of Terms

**Date version issued**
: yyyy-mm-dd

**Date created**
: yyyy-mm-dd

**Part of TDWG Standard**
: <http://www.tdwg.org/standards/643>

**This version**
: <http://rs.tdwg.org/ltc/doc/list/yyyy-mm-dd>

**Latest version**
: <http://rs.tdwg.org/ltc/doc/list/>

**Abstract**
: Latimer Core (LtC) is a data standard designed to support the representation, discovery and communication of natural science collections. A Latimer Core record may represent a grouping of objects at any level of granularity above the level of a single object, from an entire collection of an institution to a few objects in a single drawer. The classes within the standard aim to allow the high-level representation of any given collection by providing a framework within which the defining characteristics shared by objects in the collection can be described. Among others, these include their taxonomic, geographic, stratigraphic and temporal coverage, and a framework for adding quantative metrics and narratives to help to quantify and describe the collections.

The creation of collection-level records is intended to promote visibility and use of items in collections that are otherwise wholly or partially undigitised at a granular level. This document contains a list of attributes of each Latimer Core term, including a documentation name, a specified URI, a recommended English label for user interfaces, a definition, and some ancillary notes.

**Contributors**
: Matt Woodburn, Kate Webbink, Janeen Jones, Sharon Grant, Deborah Paul, Maarten Trekels, Quentin Groom, Sarah Vincent, Gabi Droege, William Ulate, Mike Trizna, Niels Raes, Jutta Buschbom

**Creator**
: TDWG Collection Descriptions (CD) Interest Group

**Bibliographic citation**
: Latimer Core Maintenance Group. 2022. Latimer Core List of Terms. Biodiversity Information Standards (TDWG). <http://rs.tdwg.org/ltc/doc/list/yyyy-mm-dd>


## 1 Introduction

### 1.1 Status of the content of this document
Sections 2 through 3 are normative, except for Table 1. In Section 4 and its subparts, the values of the Normative URI, Definition, Required, and Repeatable are normative. The value of Usage (if it exists for a given term) is normative in that it specifies how a borrowed term should be used as part of Latimer Core. The values of Term Name is non-normative, although one can expect that the namespace abbreviation prefix is one commonly used for the term namespace. Labels and the values of all other properties (such as notes) are non-normative.

### 1.2 RFC 2119 key words
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### 1.3 Categories of terms
A Latimer Core (LtC) record is a description of a grouping of collection objects using the LtC vocabularies. It is primarily focused on the description of natural science collections, but not exclusively. The terms in this document can be loosely grouped into several categories.

**Terms describing the nature and scope of the collection objects within the group.** These include a number of terms within `ltc:ObjectGroup` class, and associated classes that provide information about the scope of the collection being described such as the `ltc:GeographicOrigin`, `dwc:GeologicalContext` and `dwc:Taxon` classes. Due to the potentially heterogeneous nature of the objects within any given group, these classes and terms will often be repeatable within a LtC record.

**Terms describing the group as a whole.** These are terms that relate to the group as a single entity, mapping to the concept of a 'collection'. They include basic information terms within the `ltc:ObjectGroup` class, such as `ltc:collectionName` and `ltc:description`, but also include terms relating to the management, accessibility and tracking of the collection such as the `ltc:CollectionHistory` class and `ltc:conditionsOfAccess` property. There is also some overlap with the generic terms in the category below, in the association of people, institutions and other organisational units with the collections.  

**Generic, reusable terms that can be applied in several contexts within the standard.** Latimer Core uses a flexible approach to the representation of concepts that may be applicable in more than one concept within the class. For example, rather than specifying a separate term for each type of relevant identifier (for collections, people, organisations, taxa and so on), LtC has a generic `ltc:Identifier` class. The type of identifier is defined in each instance of the class using the `rdf:identifierType` property, and the object to which it relates (such as an instance of `ltc:Person` or `ltc:OrganisationalUnit`) is defined by the association with that class in the dataset. A similar approach applies to other classes in LtC, including `ltc:Address`, `ltc:ContactDetail` and `ltc:OrganisationalUnit`. Similarly, `ltc:Person` is reusable, but uses the `ltc:PersonRole` class to associate the person with instances of other classes in a particular role context (e.g. 'Collector', 'Record creator').

**Terms providing machine-readable metadata about the LtC record.** These terms are predominantly found in the `ltc:RecordLevel` class, and are intended to support the publication of LtC records as FAIR (Findable, Accessible, Interoperable and Reusable) data. These include support for persistent record identifiers (`dc:PID`) and licensing and rights (`dc:license`, `dc:recordRights` and `dc:rightsHolder`). The `ltc:CollectionDescriptionScheme` class also fits into this category, and is intended to provide a mechanism to group LtC records under a common scheme and profile that allows the data to be appropriately aggregated and validated.

## 2 Borrowed Vocabulary
When terms are borrowed from other vocabularies, LtC uses the URIs, common abbreviations, and namespace prefixes in use in those vocabularies. The URIs are normative, but abbreviations and namespace prefixes have no impact except as an aid to reading the documentation.

Table 1. Vocabularies from which terms have been borrowed (non-normative)

Note: URIs for terms in most of these namespaces do not dereference to anything.  The authoritative documentation can be obtained by clicking on the vocabulary names in the table.

| Vocabulary | Abbreviation | Namespaces and abbreviations |
|------------|--------------|------------------------------|
| [Darwin Core](https://dwc.tdwg.org/terms/) | DwC         | `dwc: = http://rs.tdwg.org/dwc/terms/`
| [Dublin Core](http://dublincore.org/documents/dcmi-terms/) | DC          | `dc: = http://purl.org/dc/elements/1.1/, dcterms: = http://purl.org/dc/terms/` |
| [Schema.org](https://schema.org/) | Schema      | `schema: =  https://schema.org/version/latest/schemaorg-current-https.rdf` |
| [Resource Description Framework](https://www.w3.org/RDF/) | RDF | `rdf: = http://www.w3.org/1999/02/22-rdf-syntax-ns#` |
| [Access to Biological Collection Data](https://abcd.tdwg.org/) | ABCD | `abcd: = https://abcd.tdwg.org/terms/` |


## 3 Namespaces, Prefixes and Term Names
The namespace of terms borrowed from other vocabularies is that of the original. The namespace of de novo LtC terms is http://rs.tdwg.org/ltc/terms/. In the table of terms, each term entry has a row with the term name. This term name is generally an “unqualified name” preceded by a widely accepted prefix designating an abbreviation for the namespace It is RECOMMENDED that implementers who need a namespace prefix for the LtC namespace use ltc. In this web document, hovering over a term in the [Index By Term Name](https://ltc.tdwg.org/termlist/#index-by-term-name) list below will reveal a complete URL that can be used in other web documents to link to this document’s treatment of that term, even if it is from a borrowed vocabulary. It is very important to note that some vocabularies, e.g those of the [Dublin Core Metadata Initiative (DCMI)](http://dublincore.org/), provide versions of the same term in two different namespaces, one providing for string values and one providing for URIs, even where that separation is simply a recommendation, not a mandate. See this [DCMI wiki entry](https://web.archive.org/web/20171126043657/https://github.com/dcmi/repository/blob/master/mediawiki_wiki/FAQ/DC_and_DCTERMS_Namespaces.md) on this topic.
### 3.1 Index By Term Name

(See also [3.2 Index By Label](#32-index-by-label))

**Address**

[ltc:Address](#ltc_Address) |
[schema:addressCountry](#schema_addressCountry) |
[schema:addressLocality](#schema_addressLocality) |
[schema:addressRegion](#schema_addressRegion) |
[schema:addressType](#schema_addressType) |
[schema:postOfficeBoxNumber](#schema_postOfficeBoxNumber) |
[schema:postalCode](#schema_postalCode) |
[schema:streetAddress](#schema_streetAddress) 

**Chronometric Age**

[dwc:ChronometricAge](#dwc_ChronometricAge) |
[dwc:chronometricAgeProtocol](#dwc_chronometricAgeProtocol) |
[dwc:chronometricAgeRemarks](#dwc_chronometricAgeRemarks) |
[dwc:chronometricAgeUncertaintyInYears](#dwc_chronometricAgeUncertaintyInYears) |
[dwc:earliestChronometricAge](#dwc_earliestChronometricAge) |
[dwc:earliestChronometricAgeReferenceSystem](#dwc_earliestChronometricAgeReferenceSystem) |
[dwc:latestChronometricAge](#dwc_latestChronometricAge) |
[dwc:latestChronometricAgeReferenceSystem](#dwc_latestChronometricAgeReferenceSystem) |
[dwc:verbatimChronometricAge](#dwc_verbatimChronometricAge) 

**Collection Description Scheme**

[ltc:CollectionDescriptionScheme](#ltc_CollectionDescriptionScheme) |
[ltc:basisOfScheme](#ltc_basisOfScheme) |
[ltc:distinctObjects](#ltc_distinctObjects) |
[ltc:schemeName](#ltc_schemeName) 

**Collection Status History**

[ltc:CollectionStatusHistory](#ltc_CollectionStatusHistory) |
[ltc:status](#ltc_status) |
[ltc:statusChangeReason](#ltc_statusChangeReason) |
[ltc:statusType](#ltc_statusType) 

**Contact Detail**

[ltc:ContactDetail](#ltc_ContactDetail) |
[ltc:contactDetailCategory](#ltc_contactDetailCategory) |
[ltc:contactDetailType](#ltc_contactDetailType) |
[ltc:contactDetailValue](#ltc_contactDetailValue) 

**Event**

[ltc:Event](#ltc_Event) |
[dwc:habitat](#dwc_habitat) |
[dwc:samplingProtocol](#dwc_samplingProtocol) |
[dwc:verbatimEventDate](#dwc_verbatimEventDate) 

**Geographic Origin**

[ltc:GeographicOrigin](#ltc_GeographicOrigin) |
[dwc:continent](#dwc_continent) |
[dwc:locality](#dwc_locality) |
[ltc:region](#ltc_region) |
[ltc:salinityType](#ltc_salinityType) |
[dwc:waterBody](#dwc_waterBody) |
[ltc:waterBodyType](#ltc_waterBodyType) 

**Geological Context**

[dwc:GeologicalContext](#dwc_GeologicalContext) |
[dwc:bed](#dwc_bed) |
[dwc:earliestAgeOrLowestStage](#dwc_earliestAgeOrLowestStage) |
[dwc:earliestEonOrLowestEonothem](#dwc_earliestEonOrLowestEonothem) |
[dwc:earliestEpochOrLowestSeries](#dwc_earliestEpochOrLowestSeries) |
[dwc:earliestEraOrLowestErathem](#dwc_earliestEraOrLowestErathem) |
[dwc:earliestPeriodOrLowestSystem](#dwc_earliestPeriodOrLowestSystem) |
[dwc:formation](#dwc_formation) |
[dwc:group](#dwc_group) |
[dwc:latestAgeOrHighestStage](#dwc_latestAgeOrHighestStage) |
[dwc:latestEonOrHighestEonothem](#dwc_latestEonOrHighestEonothem) |
[dwc:latestEpochOrHighestSeries](#dwc_latestEpochOrHighestSeries) |
[dwc:latestEraOrHighestErathem](#dwc_latestEraOrHighestErathem) |
[dwc:latestPeriodOrHighestSystem](#dwc_latestPeriodOrHighestSystem) |
[dwc:member](#dwc_member) 

**Identifier**

[ltc:Identifier](#ltc_Identifier) |
[dcterms:identifier](#dcterms_identifier) |
[ltc:identifierType](#ltc_identifierType) |
[dcterms:source](#dcterms_source) 

**Measurement or Fact**

[dwc:MeasurementOrFact](#dwc_MeasurementOrFact) |
[dwc:measurementAccuracy](#dwc_measurementAccuracy) |
[ltc:measurementDerivation](#ltc_measurementDerivation) |
[ltc:measurementFactText](#ltc_measurementFactText) |
[dwc:measurementMethod](#dwc_measurementMethod) |
[dwc:measurementRemarks](#dwc_measurementRemarks) |
[dwc:measurementType](#dwc_measurementType) |
[dwc:measurementUnit](#dwc_measurementUnit) |
[dwc:measurementValue](#dwc_measurementValue) 

**Object Classification**

[ltc:ObjectClassification](#ltc_ObjectClassification) |
[ltc:objectClassificationLevel](#ltc_objectClassificationLevel) |
[ltc:objectClassificationName](#ltc_objectClassificationName) |
[ltc:objectClassificationParent](#ltc_objectClassificationParent) 

**Object Group**

[ltc:ObjectGroup](#ltc_ObjectGroup) |
[ltc:baseTypeOfCollection](#ltc_baseTypeOfCollection) |
[ltc:collectionManagementSystem](#ltc_collectionManagementSystem) |
[ltc:collectionName](#ltc_collectionName) |
[ltc:conditionsOfAccess](#ltc_conditionsOfAccess) |
[ltc:currentCollection](#ltc_currentCollection) |
[dwc:degreeOfEstablishment](#dwc_degreeOfEstablishment) |
[dc:description](#dc_description) |
[ltc:discipline](#ltc_discipline) |
[ltc:knownToContainTypes](#ltc_knownToContainTypes) |
[ltc:material](#ltc_material) |
[ltc:objectType](#ltc_objectType) |
[ltc:period](#ltc_period) |
[ltc:preparationType](#ltc_preparationType) |
[ltc:preservationMethod](#ltc_preservationMethod) |
[ltc:preservationMode](#ltc_preservationMode) |
[ltc:typeOfCollection](#ltc_typeOfCollection) 

**Organisational Unit**

[ltc:OrganisationalUnit](#ltc_OrganisationalUnit) |
[ltc:organisationalUnitName](#ltc_organisationalUnitName) |
[ltc:organisationalUnitType](#ltc_organisationalUnitType) 

**Person**

[ltc:Person](#ltc_Person) |
[schema:additionalName](#schema_additionalName) |
[schema:familyName](#schema_familyName) |
[abcd:fullName](#abcd_fullName) |
[schema:givenName](#schema_givenName) 

**Person Role**

[ltc:PersonRole](#ltc_PersonRole) |
[ltc:endedAtTime](#ltc_endedAtTime) |
[ltc:role](#ltc_role) |
[ltc:startedAtTime](#ltc_startedAtTime) 

**Record Level**

[ltc:RecordLevel](#ltc_RecordLevel) |
[ltc:collectionDescriptionPID](#ltc_collectionDescriptionPID) |
[ltc:derivedCollection](#ltc_derivedCollection) |
[dc:license](#dc_license) |
[dc:recordRights](#dc_recordRights) |
[dc:rightsHolder](#dc_rightsHolder) 

**Reference**

[dwc:Reference](#dwc_Reference) |
[abcd:referenceDetails](#abcd_referenceDetails) |
[abcd:referenceText](#abcd_referenceText) |
[ltc:referenceType](#ltc_referenceType) |
[abcd:resourceURI](#abcd_resourceURI) 

**Resource Relationship**

[dwc:ResourceRelationship](#dwc_ResourceRelationship) |
[dwc:relatedResourceID](#dwc_relatedResourceID) |
[ltc:relatedResourceName](#ltc_relatedResourceName) |
[dwc:relationshipAccordingTo](#dwc_relationshipAccordingTo) |
[dwc:relationshipEstablishedDate](#dwc_relationshipEstablishedDate) |
[dwc:relationshipOfResource](#dwc_relationshipOfResource) |
[dwc:relationshipRemarks](#dwc_relationshipRemarks) |
[dwc:resourceID](#dwc_resourceID) |
[dwc:resourceRelationshipID](#dwc_resourceRelationshipID) 

**Scheme Measurement Or Fact**

[ltc:SchemeMeasurementOrFact](#ltc_SchemeMeasurementOrFact) |
[ltc:mandatoryMetric](#ltc_mandatoryMetric) |
[ltc:repeatableMetric](#ltc_repeatableMetric) |
[ltc:schemeMeasurementType](#ltc_schemeMeasurementType) 

**Scheme Term**

[ltc:SchemeTerm](#ltc_SchemeTerm) |
[ltc:mandatoryTerm](#ltc_mandatoryTerm) |
[ltc:repeatableTerm](#ltc_repeatableTerm) |
[ltc:termName](#ltc_termName) 

**Storage Location**

[ltc:StorageLocation](#ltc_StorageLocation) |
[ltc:locationName](#ltc_locationName) |
[ltc:locationType](#ltc_locationType) 

**Taxon**

[dwc:Taxon](#dwc_Taxon) |
[dwc:genus](#dwc_genus) |
[dwc:kingdom](#dwc_kingdom) |
[dwc:scientificName](#dwc_scientificName) |
[dwc:taxonRank](#dwc_taxonRank) 

**Temporal Coverage**

[ltc:TemporalCoverage](#ltc_TemporalCoverage) |
[ltc:temporalCoverageEndDate](#ltc_temporalCoverageEndDate) |
[ltc:temporalCoverageStartDate](#ltc_temporalCoverageStartDate) |
[ltc:temporalCoverageType](#ltc_temporalCoverageType) 

### 3.2 Index By Label

(See also [3.1 Index By Term Name](#31-index-by-term-name))

**Address**

[Address](#ltc_Address) |
[Address Country](#schema_addressCountry) |
[Address Locality](#schema_addressLocality) |
[Address Region](#schema_addressRegion) |
[Address Type](#schema_addressType) |
[Post Office Box Number](#schema_postOfficeBoxNumber) |
[Postal Code](#schema_postalCode) |
[Street Address](#schema_streetAddress) 

**Chronometric Age**

[Chronometric Age](#dwc_ChronometricAge) |
[Chronometric Age Protocol](#dwc_chronometricAgeProtocol) |
[Chronometric Age Remarks](#dwc_chronometricAgeRemarks) |
[Chronometric Age Uncertainty In Years](#dwc_chronometricAgeUncertaintyInYears) |
[Earliest Chronometric Age](#dwc_earliestChronometricAge) |
[Earliest Chronometric Age Reference System](#dwc_earliestChronometricAgeReferenceSystem) |
[Latest Chronometric Age](#dwc_latestChronometricAge) |
[Latest Chronometric Age Reference System](#dwc_latestChronometricAgeReferenceSystem) |
[Verbatim Chronometric Age](#dwc_verbatimChronometricAge) 

**Collection Description Scheme**

[Basis Of Scheme](#ltc_basisOfScheme) |
[Collection Description Scheme](#ltc_CollectionDescriptionScheme) |
[Distinct Objects](#ltc_distinctObjects) |
[Scheme Name](#ltc_schemeName) 

**Collection Status History**

[Collection Status History](#ltc_CollectionStatusHistory) |
[Status](#ltc_status) |
[Status Change Reason](#ltc_statusChangeReason) |
[Status Type](#ltc_statusType) 

**Contact Detail**

[Contact Detail](#ltc_ContactDetail) |
[Contact Detail Category](#ltc_contactDetailCategory) |
[Contact Detail Type](#ltc_contactDetailType) |
[Contact Detail Value](#ltc_contactDetailValue) 

**Event**

[Event](#ltc_Event) |
[Habitat](#dwc_habitat) |
[Sampling Protocol](#dwc_samplingProtocol) |
[Verbatim Event Date](#dwc_verbatimEventDate) 

**Geographic Origin**

[Continent](#dwc_continent) |
[Geographic Origin](#ltc_GeographicOrigin) |
[Locality](#dwc_locality) |
[Region](#ltc_region) |
[Salinity Type](#ltc_salinityType) |
[Water Body](#dwc_waterBody) |
[Waterbody Type](#ltc_waterBodyType) 

**Geological Context**

[Bed](#dwc_bed) |
[Earliest Age Or Lowest Stage](#dwc_earliestAgeOrLowestStage) |
[Earliest Eon Or Lowest Eonothem](#dwc_earliestEonOrLowestEonothem) |
[Earliest Epoch Or Lowest Series](#dwc_earliestEpochOrLowestSeries) |
[Earliest Era Or Lowest Erathem](#dwc_earliestEraOrLowestErathem) |
[Earliest Period Or Lowest System](#dwc_earliestPeriodOrLowestSystem) |
[Formation](#dwc_formation) |
[Geological Context](#dwc_GeologicalContext) |
[Group](#dwc_group) |
[Latest Age Or Highest Stage](#dwc_latestAgeOrHighestStage) |
[Latest Eon Or Highest Eonothem](#dwc_latestEonOrHighestEonothem) |
[Latest Epoch Or Highest Series](#dwc_latestEpochOrHighestSeries) |
[Latest Era Or Highest Erathem](#dwc_latestEraOrHighestErathem) |
[Latest Period Or Highest System](#dwc_latestPeriodOrHighestSystem) |
[Member](#dwc_member) 

**Identifier**

[Identifier](#ltc_Identifier) |
[Identifier Source](#dcterms_source) |
[Identifier Type](#ltc_identifierType) 

**Measurement or Fact**

[Fact or Narrative Text](#ltc_measurementFactText) |
[Measurement Derivation](#ltc_measurementDerivation) |
[Measurement Method](#dwc_measurementMethod) |
[Measurement Remarks](#dwc_measurementRemarks) |
[Measurement Type](#dwc_measurementType) |
[Measurement Unit](#dwc_measurementUnit) |
[Measurement Value](#dwc_measurementValue) |
[Measurement or Fact](#dwc_MeasurementOrFact) 

**Object Classification**

[Object Classification](#ltc_ObjectClassification) |
[Object Classification Level](#ltc_objectClassificationLevel) |
[Object Classification Name](#ltc_objectClassificationName) |
[Object Classification Parent](#ltc_objectClassificationParent) 

**Object Group**

[Base Type Of Collection](#ltc_baseTypeOfCollection) |
[Collection Management System](#ltc_collectionManagementSystem) |
[Collection Name](#ltc_collectionName) |
[Conditions of Access](#ltc_conditionsOfAccess) |
[Current Collection](#ltc_currentCollection) |
[Degree of Establishment](#dwc_degreeOfEstablishment) |
[Description](#dc_description) |
[Discipline](#ltc_discipline) |
[Known To Contain Types](#ltc_knownToContainTypes) |
[Material](#ltc_material) |
[Object Group](#ltc_ObjectGroup) |
[Object Type](#ltc_objectType) |
[Period](#ltc_period) |
[Preparation Type](#ltc_preparationType) |
[Preservation Method](#ltc_preservationMethod) |
[Preservation Mode](#ltc_preservationMode) |
[Type Of Collection](#ltc_typeOfCollection) 

**Organisational Unit**

[Organisational Unit](#ltc_OrganisationalUnit) |
[Organisational Unit Name](#ltc_organisationalUnitName) |
[Organisational Unit Type](#ltc_organisationalUnitType) 

**Person**

[Additional Name](#schema_additionalName) |
[Family Name](#schema_familyName) |
[Full Name](#abcd_fullName) |
[Given Name](#schema_givenName) |
[Person](#ltc_Person) 

**Person Role**

[Ended At Time](#ltc_endedAtTime) |
[Person Role](#ltc_PersonRole) |
[Role](#ltc_role) |
[Started At Time](#ltc_startedAtTime) 

**Record Level**

[Collection Description PID](#ltc_collectionDescriptionPID) |
[Derived Collection](#ltc_derivedCollection) |
[License](#dc_license) |
[Record Level](#ltc_RecordLevel) |
[Record Rights](#dc_recordRights) |
[Rights Holder](#dc_rightsHolder) 

**Reference**

[Reference](#dwc_Reference) |
[Reference Details](#abcd_referenceDetails) |
[Reference Text](#abcd_referenceText) |
[Reference Type](#ltc_referenceType) |
[Resource URI](#abcd_resourceURI) 

**Resource Relationship**

[Related Resource ID](#dwc_relatedResourceID) |
[Related Resource Name](#ltc_relatedResourceName) |
[Relationship According To](#dwc_relationshipAccordingTo) |
[Relationship Established Date](#dwc_relationshipEstablishedDate) |
[Relationship Of Resource](#dwc_relationshipOfResource) |
[Relationship Remarks](#dwc_relationshipRemarks) |
[Resource ID](#dwc_resourceID) |
[Resource Relationship](#dwc_ResourceRelationship) |
[Resource Relationship ID](#dwc_resourceRelationshipID) 

**Scheme Measurement Or Fact**

[Mandatory Metric](#ltc_mandatoryMetric) |
[Repeatable Metric](#ltc_repeatableMetric) |
[Scheme Measurement Or Fact](#ltc_SchemeMeasurementOrFact) |
[Scheme Measurement Type](#ltc_schemeMeasurementType) 

**Scheme Term**

[Mandatory Term](#ltc_mandatoryTerm) |
[Repeatable Term](#ltc_repeatableTerm) |
[Scheme Term](#ltc_SchemeTerm) |
[Term Name](#ltc_termName) 

**Storage Location**

[Location Name](#ltc_locationName) |
[Location Type](#ltc_locationType) |
[Storage Location](#ltc_StorageLocation) 

**Taxon**

[Genus](#dwc_genus) |
[Kingdom](#dwc_kingdom) |
[Scientific Name](#dwc_scientificName) |
[Taxon](#dwc_Taxon) |
[Taxon Rank](#dwc_taxonRank) 

**Temporal Coverage**

[Temporal Coverage](#ltc_TemporalCoverage) |
[Temporal Coverage End Date](#ltc_temporalCoverageEndDate) |
[Temporal Coverage Start Date](#ltc_temporalCoverageStartDate) |
[Temporal Coverage Type](#ltc_temporalCoverageType) 

## 4 Vocabulary
### 4.1 Address

A physical postal address for an organisational unit or person.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_Address"></a>Term Name  ltc:Address</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/Address">http://rs.tdwg.org/ltc/terms/Address</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/Address-2022-05-10">http://rs.tdwg.org/ltc/terms/version/Address-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Address</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A physical postal address for an organisational unit or person.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_addressCountry"></a>Term Name  schema:addressCountry</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/addressCountry">https://schema.org/addressCountry</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Address Country</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The country. For example, USA. You can also provide the two-letter ISO 3166-1 alpha-2 country code.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Denmark</code>, <code>Colombia</code>, <code>España</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_addressLocality"></a>Term Name  schema:addressLocality</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/addressLocality">https://schema.org/addressLocality</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Address Locality</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The locality in which the street address is, and which is in the region. For example which city, Mountain View.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The locality in which the address is located. AddressLocality is a more specific geographic area than addressRegion.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Holzminden</code>, <code>Araçatuba</code>, <code>Ga-Segonyana</code>, <code>Mountain View</code>, <code>Coventry</code>, <code>Tokyo</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_addressRegion"></a>Term Name  schema:addressRegion</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/addressRegion">https://schema.org/addressRegion</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Address Region</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The region in which the locality is, and which is in the country. For example, California or another appropriate first-level Administrative division.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Missoula</code>, <code>Los Lagos</code>, <code>Mataró</code>, <code>Guangdong</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_addressType"></a>Term Name  schema:addressType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/addressType">https://schema.org/addressType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Address Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A person or organization can have different contact points, for different purposes. For example, a sales contact point, a PR contact point and so on. This property is used to specify the kind of contact point.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A person or organization can have different addresses, for different purposes. For example, a postal address, a loan address, an address for visits and so on. This property is used to specify the kind of address.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Physical</code>, <code>Postal</code>, <code>Loans</code>, <code>Visits</code>, <code>Home</code>, <code>Work</code>, <code>Main</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_postOfficeBoxNumber"></a>Term Name  schema:postOfficeBoxNumber</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/postOfficeBoxNumber">https://schema.org/postOfficeBoxNumber</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Post Office Box Number</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The post office box number for PO box addresses.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>PO Box 7169</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_postalCode"></a>Term Name  schema:postalCode</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/postalCode">https://schema.org/postalCode</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Postal Code</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The postal code. For example, 94043.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>32308</code>, <code>SW7 5HD</code>, <code>10115</code>, <code>3080</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_streetAddress"></a>Term Name  schema:streetAddress</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/streetAddress">https://schema.org/streetAddress</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Street Address</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The street address. For example, 1600 Amphitheatre Pkwy.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Invalidenstraße 43</code>, <code>1400 S. Du Sable Lake Shore Dr</code>, <code>960 Carling Avenue</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.2 Chronometric Age

The age of a specimen or related materials that is generated from a dating assay. This is a categorical term (class) to organize the other chronometric age properties and does not ever have values.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_ChronometricAge"></a>Term Name  dwc:ChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/ChronometricAge">http://rs.tdwg.org/dwc/terms/ChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The age of a specimen or related materials that is generated from a dating assay.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This is a categorical term (class) to organize the other chronometric age properties and does not ever have values.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_chronometricAgeProtocol"></a>Term Name  dwc:chronometricAgeProtocol</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/chronometricAgeProtocol">http://rs.tdwg.org/dwc/terms/chronometricAgeProtocol</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age Protocol</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A description of or reference to the methods used to determine the ChronometricAge.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>1510 +/- 25 14C yr BP</code>, <code>16.26 Ma +/- 0.016</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_chronometricAgeRemarks"></a>Term Name  dwc:chronometricAgeRemarks</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/chronometricAgeRemarks">http://rs.tdwg.org/dwc/terms/chronometricAgeRemarks</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age Remarks</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Notes or comments about the ChronometricAge.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Beta Analytic number: 323913</code> <code>One of the Crassostrea virginica right valve specimens from North Midden Feature 17 was chosen for AMS dating, but it is unclear exactly which specimen it was.</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_chronometricAgeUncertaintyInYears"></a>Term Name  dwc:chronometricAgeUncertaintyInYears</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/chronometricAgeUncertaintyInYears">http://rs.tdwg.org/dwc/terms/chronometricAgeUncertaintyInYears</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age Uncertainty In Years</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The temporal uncertainty of the earliestChronometricAge and latestChronometicAge in years.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The expected unit for this field is years. The value in this field is number of years before and after the values given in the earliest and latest chronometric age fields within which the actual values are estimated to be.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>100</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_earliestChronometricAge"></a>Term Name  dwc:earliestChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/earliestChronometricAge">http://rs.tdwg.org/dwc/terms/earliestChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Earliest Chronometric Age</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The maximum/earliest/oldest possible age of a specimen as determined by a dating method.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The expected unit for this field is years. This field, if populated, must have an associated earliestChronometricAgeReferenceSystem.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>100</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_earliestChronometricAgeReferenceSystem"></a>Term Name  dwc:earliestChronometricAgeReferenceSystem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/earliestChronometricAgeReferenceSystem">http://rs.tdwg.org/dwc/terms/earliestChronometricAgeReferenceSystem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Earliest Chronometric Age Reference System</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The reference system associated with the earliestChronometricAge.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>kya</code>, <code>mya</code>, <code>BP</code>, <code>AD</code>, <code>BCE</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_latestChronometricAge"></a>Term Name  dwc:latestChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/latestChronometricAge">http://rs.tdwg.org/dwc/terms/latestChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Latest Chronometric Age</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The minimum/latest/youngest possible age of a specimen as determined by a dating method.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The minimum/latest/youngest possible age of an object in the collection as determined by a dating method.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The expected unit for this field is years. This field, if populated, must have an associated latestChronometricAgeReferenceSystem.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>27</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_latestChronometricAgeReferenceSystem"></a>Term Name  dwc:latestChronometricAgeReferenceSystem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/latestChronometricAgeReferenceSystem">http://rs.tdwg.org/dwc/terms/latestChronometricAgeReferenceSystem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Latest Chronometric Age Reference System</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The reference system associated with the latestChronometricAge.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to use a controlled vocabulary.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>kya</code>, <code>mya</code>, <code>BP</code>, <code>AD</code>, <code>BCE</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_verbatimChronometricAge"></a>Term Name  dwc:verbatimChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/verbatimChronometricAge">http://rs.tdwg.org/dwc/terms/verbatimChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Verbatim Chronometric Age</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The verbatim age for a specimen, whether reported by a dating assay, associated references, or legacy information.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The verbatim age for the objects in the collection, whether reported by a dating assay, associated references, or legacy information.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>For example, this could be the radiocarbon age as given in an AMS dating report. This could also be simply what is reported as the age of a specimen in legacy collections data.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>27 BC to 14 AD</code>, <code>stratigraphically pre-1104</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.3 Collection Description Scheme

A grouping of multiple ObjectGroups for a particular use case, purpose or implementation. Where the same objects within the same collection might be described by more than one ObjectGroup for different purposes (for examples, a 'Darwin Fossil Mammals' collection description might overlap with a 'Offsite Palaeontology' collection description), this class can be used to distinguish between them and avoid double-counting of metrics in queries against the data.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_CollectionDescriptionScheme"></a>Term Name  ltc:CollectionDescriptionScheme</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/CollectionDescriptionScheme">http://rs.tdwg.org/ltc/terms/CollectionDescriptionScheme</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/CollectionDescriptionScheme-2022-05-10">http://rs.tdwg.org/ltc/terms/version/CollectionDescriptionScheme-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Collection Description Scheme</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A grouping of multiple ObjectGroups for a particular use case, purpose or implementation.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Where the same objects within the same collection might be described by more than one ObjectGroup for different purposes (for examples, a 'Darwin Fossil Mammals' collection description might overlap with a 'Offsite Palaeontology' collection description), this class can be used to distinguish between them and avoid double-counting of metrics in queries against the data.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_basisOfScheme"></a>Term Name  ltc:basisOfScheme</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/basisOfScheme">http://rs.tdwg.org/ltc/terms/basisOfScheme</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/basisOfScheme-2022-05-10">http://rs.tdwg.org/ltc/terms/version/basisOfScheme-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Basis Of Scheme</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A summary of the basis or purpose for the CollectionDescriptionScheme.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property is intended to summarise the reason for grouping a number of ObjectGroups within the CollectionDescriptionScheme, and the purpose for which the data is intended to be used. This may also be reflected in the terms and metrics defined using the SchemeTerm and SchemeMeasurementOrFact classes respectively. Using this approach, standard and reusable profiles within the wider Latimer Core standard may be constructed for common collection descriptions use cases.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Accession</code>, <code>Inventory</code>, <code>Expedition</code>, <code>Digitisation planning</code>, <code>Collections assessment</code>, <code>Institution</code>, <code>Collections registry</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_distinctObjects"></a>Term Name  ltc:distinctObjects</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/distinctObjects">http://rs.tdwg.org/ltc/terms/distinctObjects</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/distinctObjects-2022-05-10">http://rs.tdwg.org/ltc/terms/version/distinctObjects-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Distinct Objects</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A flag to designate whether a physical object may be described by more than one ObjectGroup within the CollectionDescriptionScheme.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>If distinctObjects is set to 'true', then no collection object should be covered by more than one object group within the CollectionDescriptionScheme.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>If distinctObjects is set to 'true', then no collection object should be covered by more than one object group within the CollectionDescriptionScheme. This is important for aggregating and reporting on metrics such as object counts, as it prevents any physical object from being counted more than once.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>true</code> <code>false</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_schemeName"></a>Term Name  ltc:schemeName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/schemeName">http://rs.tdwg.org/ltc/terms/schemeName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/schemeName-2022-05-10">http://rs.tdwg.org/ltc/terms/version/schemeName-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Scheme Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A short descriptive name given to the CollectionDescriptionScheme.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>NHM Collections Inventory</code>, <code>Index Herbariorum</code>, <code>European Darwin Collections</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.4 Collection Status History

A record of current and past statuses of the object group and the reason for status changes. Use this class to record the history of and reason for changes in the status of the described collection. Types of status described by this class may, for example, include ownership, management, accessibility or accrual policy over time. Dates reflecting the start and end of the status described by this class should be recorded using an instance of TemporalCoverage. If temporalCoverageEndDate is empty, the status can be inferred to be the current status of the collection.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_CollectionStatusHistory"></a>Term Name  ltc:CollectionStatusHistory</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/CollectionStatusHistory">http://rs.tdwg.org/ltc/terms/CollectionStatusHistory</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/CollectionStatusHistory-2022-05-10">http://rs.tdwg.org/ltc/terms/version/CollectionStatusHistory-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Collection Status History</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A record of current and past statuses of the object group and the reason for status changes.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Use this class to record the history of and reason for changes in the status of the described collection. Types of status described by this class may, for example, include ownership, management, accessibility or accrual policy over time. Dates reflecting the start and end of the status described by this class should be recorded using an instance of TemporalCoverage. If temporalCoverageEndDate is empty, the status can be inferred to be the current status of the collection.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_status"></a>Term Name  ltc:status</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/status">http://rs.tdwg.org/ltc/terms/status</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/status-2022-05-10">http://rs.tdwg.org/ltc/terms/version/status-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Status</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The development status of the collection during a specified period.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The values/vocabularies for a status are predicated by the statusType. The in the examples mentioned terms are a cumulative list of terms associated with several different statusTypes.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Complete</code>, <code>In part</code>, <code>Developing</code>, <code>Closed</code>, <code>Active growth</code>, <code>Consumable</code>, <code>Decreasing</code>, <code>Lost</code>, <code>Missing</code>, <code>Passive growth</code>, <code>Static</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_statusChangeReason"></a>Term Name  ltc:statusChangeReason</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/statusChangeReason">http://rs.tdwg.org/ltc/terms/statusChangeReason</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/statusChangeReason-2022-05-10">http://rs.tdwg.org/ltc/terms/version/statusChangeReason-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Status Change Reason</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An explanation of why the collection transitioned to the value set in the status property.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>statusChangeReason should be aligned with the value of statusType.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Pest infestation</code>, <code>Exchange</code>, <code>Transfer</code>, <code>Return to country of origin</code>, <code>Worldwide pandemic</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_statusType"></a>Term Name  ltc:statusType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/statusType">http://rs.tdwg.org/ltc/terms/statusType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/statusType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/statusType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Status Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A top-level classification of the different categories of status that can be applied to the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>statusType forms the top level of a two-level hierarchy with the status property.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Stewardship</code>, <code>Accessibility</code>, <code>Completeness</code>, <code>Collection dynamics</code>, <code>Organizational</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.5 Contact Detail

Details of a method by which an entity such as a Person or OrganisationalUnit may be contacted. The Address class should be used to store physical or postal addresses. For all other types of contact details, this class should be used.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_ContactDetail"></a>Term Name  ltc:ContactDetail</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/ContactDetail">http://rs.tdwg.org/ltc/terms/ContactDetail</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/ContactDetail-2022-05-10">http://rs.tdwg.org/ltc/terms/version/ContactDetail-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Contact Detail</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Details of a method by which an entity such as a Person or OrganisationalUnit may be contacted.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The Address class should be used to store physical or postal addresses. For all other types of contact details, this class should be used.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_contactDetailCategory"></a>Term Name  ltc:contactDetailCategory</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/contactDetailCategory">http://rs.tdwg.org/ltc/terms/contactDetailCategory</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/contactDetailCategory-2022-05-10">http://rs.tdwg.org/ltc/terms/version/contactDetailCategory-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Contact Detail Category</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The method of contact to which the contact detail applies.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended practice is to use a controlled vocabulary.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Email</code>, <code>Phone</code>, <code>Twitter handle</code>, <code>GitHub handle</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_contactDetailType"></a>Term Name  ltc:contactDetailType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/contactDetailType">http://rs.tdwg.org/ltc/terms/contactDetailType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/contactDetailType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/contactDetailType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Contact Detail Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The type of contact detail, which can be used to distinguish between multiple contact details of the same contactDetailCategory.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Home</code>, <code>Personal</code>, <code>Work</code>, <code>General enquiries</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_contactDetailValue"></a>Term Name  ltc:contactDetailValue</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/contactDetailValue">http://rs.tdwg.org/ltc/terms/contactDetailValue</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/contactDetailValue-2022-05-10">http://rs.tdwg.org/ltc/terms/version/contactDetailValue-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Contact Detail Value</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The value of the contact detail, such as the phone number or email address.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>01234 567891</code>, <code>someone@example.org</code>, <code>@github_user</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.6 Event

An action that occurs at some location during some time. From dwc Class event (http://rs.tdwg.org/dwc/terms/version/Event-2018-09-06). Examples include: A specimen collection process. A camera trap image capture. A marine trawl.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_Event"></a>Term Name  ltc:Event</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/Event">http://rs.tdwg.org/ltc/terms/Event</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/Event-2022-05-10">http://rs.tdwg.org/ltc/terms/version/Event-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Event</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An action that occurs at some location during some time.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>From dwc Class event (<a href="http://rs.tdwg.org/dwc/terms/version/Event-2018-09-06">http://rs.tdwg.org/dwc/terms/version/Event-2018-09-06</a>). Examples include: A specimen collection process. A camera trap image capture. A marine trawl.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_habitat"></a>Term Name  dwc:habitat</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/habitat">http://rs.tdwg.org/dwc/terms/habitat</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Habitat</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A category or description of the habitat in which the Event occurred.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>oak savanna</code>, <code>pre-cordilleran steppe</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_samplingProtocol"></a>Term Name  dwc:samplingProtocol</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/samplingProtocol">http://rs.tdwg.org/dwc/terms/samplingProtocol</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Sampling Protocol</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The name of, reference to, or description of the method or protocol used during an Event</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The name of, reference to, or description of the method or protocol used to gather objects in the collection.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>UV light trap</code> <code>mist net</code> <code>bottom trawl</code> <code>ad hoc observation</code> <code>Penguins from space: faecal stains reveal the location of emperor penguin colonies, <a href="https://doi.org/10.1111/j.1466-8238.2009.00467.x">https://doi.org/10.1111/j.1466-8238.2009.00467.x</a></code> <code>Takats et al. 2001. Guidelines for Nocturnal Owl Monitoring in North America. Beaverhill Bird Observatory and Bird Studies Canada, Edmonton, Alberta. 32 pp., <a href="http://www.bsc-eoc.org/download/Owl.pdf">http://www.bsc-eoc.org/download/Owl.pdf</a></code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2021-07-15_34">http://rs.tdwg.org/decisions/decision-2021-07-15_34</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_verbatimEventDate"></a>Term Name  dwc:verbatimEventDate</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/verbatimEventDate">http://rs.tdwg.org/dwc/terms/verbatimEventDate</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Verbatim Event Date</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The verbatim original representation of the date and time information for an Event.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>spring 1910</code>, <code>Marzo 2002</code>, <code>1999-03-XX</code>, <code>17IV1934</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.7 Geographic Origin

The geographic location from which objects associated with the ObjectGroup were collected.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_GeographicOrigin"></a>Term Name  ltc:GeographicOrigin</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/GeographicOrigin">http://rs.tdwg.org/ltc/terms/GeographicOrigin</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/GeographicOrigin-2022-05-10">http://rs.tdwg.org/ltc/terms/version/GeographicOrigin-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Geographic Origin</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The geographic location from which objects associated with the ObjectGroup were collected.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_continent"></a>Term Name  dwc:continent</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/continent">http://rs.tdwg.org/dwc/terms/continent</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Continent</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The name of the continent in which the Location occurs.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The name of the continent from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Based on best practice Getty Thesaurus of Geographic Names. --> <a href="http://www.getty.edu/vow/TGNHierarchy?find=&place=&nation=&english=Y&subjectid=7029392">http://www.getty.edu/vow/TGNHierarchy?find=&place=&nation=&english=Y&subjectid=7029392</a>. For cultural collections such as economic botany use the Region field to record things like Pacific to replace Oceania.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Africa</code>, <code>Antarctica</code>, <code>Asia</code>, <code>Europe</code>, <code>North America</code>, <code>Oceania</code>, <code>South America</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_locality"></a>Term Name  dwc:locality</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/locality">http://rs.tdwg.org/dwc/terms/locality</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Locality</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The specific description of the place. Less specific geographic information can be provided in other geographic terms (higherGeography, continent, country, stateProvince, county, municipality, waterBody, island, islandGroup). This term may contain information modified from the original to correct perceived errors or standardize the description.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The specific description of the place from which objects in the collection originated. Less specific geographic information can be provided in other geographic terms (higherGeography, continent, country, stateProvince, county, municipality, waterBody, island, islandGroup). This term may contain information modified from the original to correct perceived errors or standardize the description.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Bariloche, 25 km NNE via Ruta Nacional 40 (=Ruta 237).</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_region"></a>Term Name  ltc:region</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/region">http://rs.tdwg.org/ltc/terms/region</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/region-2022-05-10">http://rs.tdwg.org/ltc/terms/version/region-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Region</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The name of a spatial region or named place of any size within an individual or multiple administrative areas.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The name of the spatial region or named place of any size within an individual or multiple administrative areas from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to use this field in situations where the administrative location fields (country, stateProvince, county, etc.) provide insufficient description. For geological collections examples include basins, provinces, and fossil deposits.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>Multi-country: <code>North European Plain</code>, Multi-state/Province: <code>Pacific Northwest</code>, Waterbody: <code>Southern</code>, Geological basins and provinces: <code>Michigan Basin</code>, <code>Mazon Creek</code>, <code>Bundenbach</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_salinityType"></a>Term Name  ltc:salinityType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/salinityType">http://rs.tdwg.org/ltc/terms/salinityType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/salinityType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/salinityType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Salinity Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A set of terms to indicate the water environment of aquatic collections.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This should not be construed as a measurement value, but as a descriptive terms to allow for searching for freshwater vs marine etc. collections.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>marine</code>, <code>fresh</code>, <code>brackish</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_waterBody"></a>Term Name  dwc:waterBody</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/waterBody">http://rs.tdwg.org/dwc/terms/waterBody</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Water Body</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The name of the water body in which the Location occurs.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The name of the water body from which objects in the the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This is intended to define the lowest water body or aquatic feature that defines the geographical constraints of aquatic collections below ocean. Suggestions for appropriate vocabularies include: HydroLAKES (<a href="https://www.hydrosheds.org/page/hydrolakes">https://www.hydrosheds.org/page/hydrolakes</a>), a database aiming to provide the shoreline polygons of all global lakes with a surface area of at least 10 ha, the 'water body' term in the OBO ontology (<a href="http://purl.obolibrary.org/obo/ENVO_00000063">http://purl.obolibrary.org/obo/ENVO_00000063</a>) and, for marine water bodies, IHO Sea Areas (<a href="http://www.vliz.be/en/imis?dasid=5444&doiid=323">http://www.vliz.be/en/imis?dasid=5444&doiid=323</a>).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Baltic Sea</code>, <code>Hudson River</code>, <code>Lago Nahuel Huapi</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_waterBodyType"></a>Term Name  ltc:waterBodyType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/waterBodyType">http://rs.tdwg.org/ltc/terms/waterBodyType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/waterBodyType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/waterBodyType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Waterbody Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A term that indicates the aquatic order of a waterbody.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td><a href="https://www.usgs.gov/mission-areas/water-resources/science/types-water">https://www.usgs.gov/mission-areas/water-resources/science/types-water</a>  <a href="https://sciencetrends.com/types-bodies-water-complete-list/">https://sciencetrends.com/types-bodies-water-complete-list/</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Ocean</code>, <code>Sea</code>, <code>Lake</code>, <code>Pond</code>, <code>River</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.8 Geological Context

Geological information, such as stratigraphy, that qualifies a region or place.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_GeologicalContext"></a>Term Name  dwc:GeologicalContext</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/GeologicalContext">http://rs.tdwg.org/dwc/terms/GeologicalContext</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Geological Context</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Geological information, such as stratigraphy, that qualifies a region or place.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2014-10-26_15">http://rs.tdwg.org/decisions/decision-2014-10-26_15</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_bed"></a>Term Name  dwc:bed</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/bed">http://rs.tdwg.org/dwc/terms/bed</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Bed</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the lithostratigraphic bed from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the lithostratigraphic bed from which the objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabulary: <a href="https://ngmdb.usgs.gov/Geolex/search">https://ngmdb.usgs.gov/Geolex/search</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Beecher Trilobite Bed</code>, <code>McAbee Fossil Beds</code>, <code>Ashfall Fossil Beds</code>  <code>Nut Beds</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_earliestAgeOrLowestStage"></a>Term Name  dwc:earliestAgeOrLowestStage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/earliestAgeOrLowestStage">http://rs.tdwg.org/dwc/terms/earliestAgeOrLowestStage</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Earliest Age Or Lowest Stage</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the earliest possible geochronologic age or lowest chronostratigraphic stage attributable to the stratigraphic horizon from which the cataloged item was collected</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the earliest possible geochronologic age or lowest chronostratigraphic stage attributable to the stratigraphic horizon from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Atlantic</code>, <code>Boreal</code>, <code>Frasnian</code>, <code>Hirnantian</code>, <code>Maastrichtian</code>, <code>Bridgerian</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_earliestEonOrLowestEonothem"></a>Term Name  dwc:earliestEonOrLowestEonothem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/earliestEonOrLowestEonothem">http://rs.tdwg.org/dwc/terms/earliestEonOrLowestEonothem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Earliest Eon Or Lowest Eonothem</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the earliest possible geochronologic eon or lowest chrono-stratigraphic eonothem or the informal name (Precambrian) attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the earliest possible geochronologic eon or lowest chrono-stratigraphic eonothem or the informal name (Precambrian) attributable to the stratigraphic horizon from which the objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Phanerozoic</code>, <code>Proterozoic</code>, <code>Arechean</code>, <code>Hadean</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_earliestEpochOrLowestSeries"></a>Term Name  dwc:earliestEpochOrLowestSeries</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/earliestEpochOrLowestSeries">http://rs.tdwg.org/dwc/terms/earliestEpochOrLowestSeries</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Earliest Epoch Or Lowest Series</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the earliest possible geochronologic epoch or lowest chronostratigraphic series attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the earliest possible geochronologic epoch or lowest chronostratigraphic series attributable to the stratigraphic horizon from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Holocene</code> <code>Pleistocene</code> <code>Ibexian</code> <code>Late Devonian</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_earliestEraOrLowestErathem"></a>Term Name  dwc:earliestEraOrLowestErathem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/earliestEraOrLowestErathem">http://rs.tdwg.org/dwc/terms/earliestEraOrLowestErathem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Earliest Era Or Lowest Erathem</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the earliest possible geochronologic era or lowest chronostratigraphic erathem attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the earliest possible geochronologic era or lowest chronostratigraphic erathem attributable to the stratigraphic horizon from which the objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Cenozoic</code> <code>Mesozoic</code>  <code>Paleozoic</code> <code>Neoproterozoic</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_earliestPeriodOrLowestSystem"></a>Term Name  dwc:earliestPeriodOrLowestSystem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/earliestPeriodOrLowestSystem">http://rs.tdwg.org/dwc/terms/earliestPeriodOrLowestSystem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Earliest Period Or Lowest System</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the earliest possible geochronologic period or lowest chronostratigraphic system attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the earliest possible geochronologic period or lowest chronostratigraphic system attributable to the stratigraphic horizon from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Neogene</code>, <code>Quaternary</code>, <code>Jurassic</code>, <code>Devonian</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_formation"></a>Term Name  dwc:formation</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/formation">http://rs.tdwg.org/dwc/terms/formation</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Formation</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the lithostratigraphic formation from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the lithostratigraphic formation from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabulary: <a href="https://ngmdb.usgs.gov/Geolex/search">https://ngmdb.usgs.gov/Geolex/search</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Notch Peak Formation</code>, <code> House Limestone</code>,  <code>Fillmore Formation</code>, <code>Redwall Limestone</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_group"></a>Term Name  dwc:group</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/group">http://rs.tdwg.org/dwc/terms/group</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Group</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the lithostratigraphic group from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the lithostratigraphic group from which the objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabulary: <a href="https://ngmdb.usgs.gov/Geolex/search">https://ngmdb.usgs.gov/Geolex/search</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Bathurst</code>, <code>Wealden</code>, <code>Elk Mound</code>, <code>Supai</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_latestAgeOrHighestStage"></a>Term Name  dwc:latestAgeOrHighestStage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/latestAgeOrHighestStage">http://rs.tdwg.org/dwc/terms/latestAgeOrHighestStage</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Latest Age Or Highest Stage</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the latest possible geochronologic age or highest chronostratigraphic stage attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the latest possible geochronologic age or highest chronostratigraphic stage attributable to the stratigraphic horizon from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Atlantic</code>, <code>Boreal</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_latestEonOrHighestEonothem"></a>Term Name  dwc:latestEonOrHighestEonothem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/latestEonOrHighestEonothem">http://rs.tdwg.org/dwc/terms/latestEonOrHighestEonothem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Latest Eon Or Highest Eonothem</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the latest possible geochronologic eon or highest chrono-stratigraphic eonothem or the informal name (Precambrian) attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the latest possible geochronologic eon or highest chrono-stratigraphic eonothem or the informal name (Precambrian) attributable to the stratigraphic horizon from which the objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Phanerozoic</code>, <code>Proterozoic</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_latestEpochOrHighestSeries"></a>Term Name  dwc:latestEpochOrHighestSeries</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/latestEpochOrHighestSeries">http://rs.tdwg.org/dwc/terms/latestEpochOrHighestSeries</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Latest Epoch Or Highest Series</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the latest possible geochronologic epoch or highest chronostratigraphic series attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the latest possible geochronologic epoch or highest chronostratigraphic series attributable to the stratigraphic horizon from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Holocene</code>, <code>Pleistocene</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_latestEraOrHighestErathem"></a>Term Name  dwc:latestEraOrHighestErathem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/latestEraOrHighestErathem">http://rs.tdwg.org/dwc/terms/latestEraOrHighestErathem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Latest Era Or Highest Erathem</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the latest possible geochronologic era or highest chronostratigraphic erathem attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the latest possible geochronologic era or highest chronostratigraphic erathem attributable to the stratigraphic horizon from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Cenozoic</code>, <code>Mesozoic</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_latestPeriodOrHighestSystem"></a>Term Name  dwc:latestPeriodOrHighestSystem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/latestPeriodOrHighestSystem">http://rs.tdwg.org/dwc/terms/latestPeriodOrHighestSystem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Latest Period Or Highest System</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the latest possible geochronologic period or highest chronostratigraphic system attributable to the stratigraphic horizon from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the latest possible geochronologic period or highest chronostratigraphic system attributable to the stratigraphic horizon from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended vocabularies: <a href="https://stratigraphy.org/chart">https://stratigraphy.org/chart</a>, <a href="https://timescalefoundation.org/resources/geowhen/index.html">https://timescalefoundation.org/resources/geowhen/index.html</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Neogene</code>, <code>Tertiary</code>, <code>Quaternary</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_member"></a>Term Name  dwc:member</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/member">http://rs.tdwg.org/dwc/terms/member</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Member</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full name of the lithostratigraphic member from which the cataloged item was collected.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full name of the lithostratigraphic member from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommend vocabulary: <a href="https://ngmdb.usgs.gov/Geolex/search">https://ngmdb.usgs.gov/Geolex/search</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Lava Dam Member</code>, <code>Hellnmaria Member</code>, <code>Francis Creek Shale</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.9 Identifier

A numeric, textual value, or reference such as an IRI, that can be used to uniquely identify the object to which it is attached. Use this class to document stable identifiers that describe the collections and associated entities being represented in the collection description. For example, person identifiers, taxon identifiers, institution identifiers, organisational unit identifiers, gazetteer identifiers. Identifiers represented by this class may be globally unique, or unique within a given context.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_Identifier"></a>Term Name  ltc:Identifier</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/Identifier">http://rs.tdwg.org/ltc/terms/Identifier</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/Identifier-2022-05-10">http://rs.tdwg.org/ltc/terms/version/Identifier-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Identifier</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A numeric, textual value, or reference such as an IRI, that can be used to uniquely identify the object to which it is attached.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Use this class to document stable identifiers that describe the collections and associated entities being represented in the collection description. For example, person identifiers, taxon identifiers, institution identifiers, organisational unit identifiers, gazetteer identifiers. Identifiers represented by this class may be globally unique, or unique within a given context.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dcterms_identifier"></a>Term Name  dcterms:identifier</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://purl.org/dc/terms/identifier">http://purl.org/dc/terms/identifier</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Identifier</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An unambiguous reference to the resource within a given context.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A textual or numeric identifier, acronym or URI that provides an unambiguous reference for an entity within a given context.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This may be a simple value or resolvable URI, and can reflect any identifier used to identify an entity (such as a collection, taxon, institution or person) included in the Collection Description.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code><a href="http://grscicoll.org/institutional-collection/osteology">http://grscicoll.org/institutional-collection/osteology</a></code>, <code><a href="https://www.gbif.org/grscicoll/collection/64232ca4-fd5a-4a3d-a1d5-ef812107472c">https://www.gbif.org/grscicoll/collection/64232ca4-fd5a-4a3d-a1d5-ef812107472c</a></code>, <code><a href="https://www.gbif.org/grscicoll/institution/52827361-5e82-43b7-b92a-f6ad98367fa5">https://www.gbif.org/grscicoll/institution/52827361-5e82-43b7-b92a-f6ad98367fa5</a></code>, <code><a href="http://sweetgum.nybg.org/science/ih/herbarium-details/?irn=126969">http://sweetgum.nybg.org/science/ih/herbarium-details/?irn=126969</a></code>, <code>10.5072/example-full</code>, <code>NHMUK-Verts</code>, <code>BGBM</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2019-12-01_19">http://rs.tdwg.org/decisions/decision-2019-12-01_19</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_identifierType"></a>Term Name  ltc:identifierType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/identifierType">http://rs.tdwg.org/ltc/terms/identifierType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/identifierType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/identifierType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Identifier Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The type and format of the value in the identifier field.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property should be used to help people and software understand how the identifier can be used (e.g. whether it's a resolvable URI) and validate the identifier based on format and composition (e.g. a valid UUID).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Acronym</code>, <code>URI</code>, <code>UUID v4</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dcterms_source"></a>Term Name  dcterms:source</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://purl.org/dc/terms/source">http://purl.org/dc/terms/source</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Identifier Source</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A related resource from which the described resource is derived.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The source or creator of the identifier.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This term refers to the organisation, framework, software or database that minted the identifier represented in the identifier property.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Index Herbariorum</code>, <code>GBIF Registry of Scientific Collections (GRSciColl)</code>, <code>CITES</code>, <code>IPEN</code>, <code>NHM UK 'Join the Dots' framework</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2019-12-01_19">http://rs.tdwg.org/decisions/decision-2019-12-01_19</a></td>
		</tr>
	</tbody>
</table>


### 4.10 Measurement or Fact

A measurement of or fact about the ObjectGroup representing the objects in the collection description, or the relationship between the ObjectGroup and an associated class. This class can be used to apply measurements, facts or narratives to the ObjectGroup as a whole, or used to qualify the relationship between the ObjectGroup and an associated attribute. For example, an ObjectGroup may contain 100 objects, of which 40 are from Europe and 60 from Africa. In this example, one MeasurementOrFact (count of 100) would be attached to the ObjectGroup, and one to each of the two relationships between the ObjectGroup and GeographicOrigin (Europe: count of 40, Africa: count of 60).<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_MeasurementOrFact"></a>Term Name  dwc:MeasurementOrFact</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/MeasurementOrFact">http://rs.tdwg.org/dwc/terms/MeasurementOrFact</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement or Fact</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A measurement of or fact about an rdfs:Resource (http://www.w3.org/2000/01/rdf-schema#Resource).</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A measurement of or fact about the ObjectGroup representing the objects in the collection description, or the relationship between the ObjectGroup and an associated class.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This class can be used to apply measurements, facts or narratives to the ObjectGroup as a whole, or used to qualify the relationship between the ObjectGroup and an associated attribute. For example, an ObjectGroup may contain 100 objects, of which 40 are from Europe and 60 from Africa. In this example, one MeasurementOrFact (count of 100) would be attached to the ObjectGroup, and one to each of the two relationships between the ObjectGroup and GeographicOrigin (Europe: count of 40, Africa: count of 60).</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2014-10-26_15">http://rs.tdwg.org/decisions/decision-2014-10-26_15</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_measurementAccuracy"></a>Term Name  dwc:measurementAccuracy</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/measurementAccuracy">http://rs.tdwg.org/dwc/terms/measurementAccuracy</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement Value</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The description of the potential error associated with the measurementValue.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The description of the potential error associated with the measurementValue applied to the collection.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>0.01</code>, <code>Normal distribution with variation of 2 m</code>, <code>Reported</code>, <code>Estimated</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_measurementDerivation"></a>Term Name  ltc:measurementDerivation</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/measurementDerivation">http://rs.tdwg.org/ltc/terms/measurementDerivation</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/measurementDerivation-2022-05-10">http://rs.tdwg.org/ltc/terms/version/measurementDerivation-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement Derivation</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An indicator as to whether the measurement, fact, characteristic, or assertion being applied to the collection was derived from reported figures or aggregated/calculated from underlying data.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>If there is more detailed information about the method by which a measurement or fact was derived, this should be captured using the measurementMethod property.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Reported</code>, <code>Calculated</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_measurementFactText"></a>Term Name  ltc:measurementFactText</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/measurementFactText">http://rs.tdwg.org/ltc/terms/measurementFactText</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/measurementFactText-2022-05-10">http://rs.tdwg.org/ltc/terms/version/measurementFactText-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Fact or Narrative Text</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The value of the qualitative fact, characteristic, or assertion being made about the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property should also be used for storing textual information about the collection within a particular context, such as narratives or comments about digitisation readiness.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>UV-light</code>, <code>Extra large</code>, <code>Level 1</code>, <code>Re-curation of this collection would be required prior to digitisation, requiring an estimated two weeks of curator time.</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_measurementMethod"></a>Term Name  dwc:measurementMethod</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/measurementMethod">http://rs.tdwg.org/dwc/terms/measurementMethod</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement Method</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A description of or reference to (publication, URI) the method or protocol used to determine the measurement, fact, characteristic, or assertion.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A brief description of or reference to (publication, URI) the method or protocol used to determine the measurement, fact, characteristic, or assertion being applied to the collection.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>DiSSCo MIDS level</code>, <code>CD Standard Metric</code>, <code><a href="https://doi.org/10.5281/zenodo.3465285">https://doi.org/10.5281/zenodo.3465285</a></code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_measurementRemarks"></a>Term Name  dwc:measurementRemarks</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/measurementRemarks">http://rs.tdwg.org/dwc/terms/measurementRemarks</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement Remarks</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Comments or notes accompanying the MeasurementOrFact.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>Comments or notes accompanying the MeasurementOrFact being applied to the collection.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Does not include on-loan material</code>, <code>Footprint includes housing</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_measurementType"></a>Term Name  dwc:measurementType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/measurementType">http://rs.tdwg.org/dwc/terms/measurementType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The nature of the measurement, fact, characteristic, or assertion.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The nature of the measurement, fact, characteristic, or assertion being made about the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to use a controlled vocabulary.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Imaged Level Percentage</code>, <code>Storage Volume</code>, <code>Object Count</code>, <code>MIDS-0 Object Count</code>, <code>Historical narrative</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_measurementUnit"></a>Term Name  dwc:measurementUnit</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/measurementUnit">http://rs.tdwg.org/dwc/terms/measurementUnit</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement Unit</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The units associated with the measurementValue.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The units associated with the measurementValue applied to the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>For some use cases, this property can also be used to reflect the type of value being stored (e.g. a count, or a percentage).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>mm</code>, <code>C</code>, <code>km</code>, <code>ha</code>, <code>count</code>, <code>percentage</code>, <code>category</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_measurementValue"></a>Term Name  dwc:measurementValue</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/measurementValue">http://rs.tdwg.org/dwc/terms/measurementValue</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Measurement Value</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The value of the measurement, fact, characteristic, or assertion.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The numeric value of the quantitative measurement being made about the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>In the Collection Description standard, this field is constrained to only accept numeric values in order to better support the aggregation of quantitative metrics. For any non-numeric values, and metrics where the scale is a numeral that cannot be used in any calculations the measurementFactText property should be used instead.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>45</code>, <code>20000</code>, <code>1</code>, <code>14.5</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.11 Object Classification

An informal classification of the type of objects within the ObjectGroup, using a hierarchical structure. This class is used to categorise the ObjectGroup according to an informal, self-referential hierarchy. For example, this can be used to create a hierarchy encompassing biological, geological and anthropological collections, where a single formal taxonomy isn't appropriate.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_ObjectClassification"></a>Term Name  ltc:ObjectClassification</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/ObjectClassification">http://rs.tdwg.org/ltc/terms/ObjectClassification</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/ObjectClassification-2022-05-10">http://rs.tdwg.org/ltc/terms/version/ObjectClassification-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Object Classification</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An informal classification of the type of objects within the ObjectGroup, using a hierarchical structure.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This class is used to categorise the ObjectGroup according to an informal, self-referential hierarchy. For example, this can be used to create a hierarchy encompassing biological, geological and anthropological collections, where a single formal taxonomy isn't appropriate.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_objectClassificationLevel"></a>Term Name  ltc:objectClassificationLevel</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/objectClassificationLevel">http://rs.tdwg.org/ltc/terms/objectClassificationLevel</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/objectClassificationLevel-2022-05-10">http://rs.tdwg.org/ltc/terms/version/objectClassificationLevel-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Object Classification Level</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The level of the ObjectClassification in the hierarchy.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>It is up to the user to name the levels to be relevant to the hierarchical classification scheme that they are defining.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Domain</code>, <code>Discipline</code>, <code>Category</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_objectClassificationName"></a>Term Name  ltc:objectClassificationName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/objectClassificationName">http://rs.tdwg.org/ltc/terms/objectClassificationName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/objectClassificationName-2022-05-10">http://rs.tdwg.org/ltc/terms/version/objectClassificationName-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Object Classification Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A short title describing this ObjectClassification as a class, unit or grouping.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This is a user-determined name given for classifying their collection. This name, expressing an assigned classification, can be part of a self-referential hierarchy.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Zoology invertebrates</code>, <code>Palaeontology</code>, <code>Extra-terrestrial</code>, <code>Archaeology</code>, <code>Seed plants</code>, <code>Birds</code>, <code>Agriculture</code>, <code>Veterinary</code>, <code>Viruses</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_objectClassificationParent"></a>Term Name  ltc:objectClassificationParent</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/objectClassificationParent">http://rs.tdwg.org/ltc/terms/objectClassificationParent</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/objectClassificationParent-2022-05-10">http://rs.tdwg.org/ltc/terms/version/objectClassificationParent-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Object Classification Parent</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The immediate parent of the ObjectClassification in a self-referential hierarchy.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>The ObjectClassification <code>Zoology</code> is the parent of the <code>Invertebrates</code> ObjectClassification; the ObjectClassification <code>Extraterrestrial</code> is the parent of the <code>Meteorites</code> ObjectClassification.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.12 Object Group

An intentionally grouped set of objects with one or more common characteristics.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_ObjectGroup"></a>Term Name  ltc:ObjectGroup</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/ObjectGroup">http://rs.tdwg.org/ltc/terms/ObjectGroup</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/ObjectGroup-2022-05-10">http://rs.tdwg.org/ltc/terms/version/ObjectGroup-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Object Group</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An intentionally grouped set of objects with one or more common characteristics.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_baseTypeOfCollection"></a>Term Name  ltc:baseTypeOfCollection</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/baseTypeOfCollection">http://rs.tdwg.org/ltc/terms/baseTypeOfCollection</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/baseTypeOfCollection-2022-05-10">http://rs.tdwg.org/ltc/terms/version/baseTypeOfCollection-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Base Type Of Collection</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>High-level term describing the fundamental nature of objects in the ObjectGroup.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>For natural history collections baseTypeOfCollection describes types of occurrences and may constrain the values available in objectType. Notes for ObjectGroups where baseTypeOfCollection is 'InformationArtefact': subsequent type properties could include hierarchical Audubon Core/Dublin Core terms, e.g. dc:type (<a href="http://purl.org/dc/elements/1.1/type">http://purl.org/dc/elements/1.1/type</a>), ac:subtype / ac:subtypeLiteral (<a href="http://rs.tdwg.org/ac/terms/subtypeLiteral">http://rs.tdwg.org/ac/terms/subtypeLiteral</a>), or (proposed) ac:3DResourceType.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>MaterialSample</code>, <code>InformationArtefact</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_collectionManagementSystem"></a>Term Name  ltc:collectionManagementSystem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/collectionManagementSystem">http://rs.tdwg.org/ltc/terms/collectionManagementSystem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/collectionManagementSystem-2022-05-10">http://rs.tdwg.org/ltc/terms/version/collectionManagementSystem-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Collection Management System</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The collection management system which is used to hold and manage the primary data for the objects contained within the ObjectGroup.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This should reflect the system or database in which the object-level records reside, rather than the source of the Collection Description data.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Specify 7</code>, <code>DINA</code>, <code>Axiell EMu</code>, <code>Arctos</code>, <code>EarthCape</code>, <code>BRAHMS</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_collectionName"></a>Term Name  ltc:collectionName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/collectionName">http://rs.tdwg.org/ltc/terms/collectionName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/collectionName-2022-05-10">http://rs.tdwg.org/ltc/terms/version/collectionName-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Collection Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A short title that summarises the collection objects contained within the ObjectGroup.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>The Leslie Hubricht Molluscan Collection</code>, <code>NHM Algae, Fungi and Plants collection</code>, <code>Crustacea & Cirripedes, Decapoda</code>, <code>Global Mesozoic and Paleozoic mollusc faunas/samples</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_conditionsOfAccess"></a>Term Name  ltc:conditionsOfAccess</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/conditionsOfAccess">http://rs.tdwg.org/ltc/terms/conditionsOfAccess</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/conditionsOfAccess-2022-05-10">http://rs.tdwg.org/ltc/terms/version/conditionsOfAccess-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Conditions of Access</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Information about who can access the collection being described or an indication of its security status.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>If available, this should be a URL to a stable policy page. For example, <a href="https://www.fieldmuseum.org/science/research/area/fossils-meteorites/fossils-meteorites-policies">https://www.fieldmuseum.org/science/research/area/fossils-meteorites/fossils-meteorites-policies</a>.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Open to the public</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_currentCollection"></a>Term Name  ltc:currentCollection</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/currentCollection">http://rs.tdwg.org/ltc/terms/currentCollection</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/currentCollection-2022-05-10">http://rs.tdwg.org/ltc/terms/version/currentCollection-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Current Collection</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A flag to indicate whether the collection still exists as a single entity.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Use this to indicate if the record describes the entirety of a known historical collection. If only part of the collection is present the value is 'false'.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>true</code> <code>false</code> <code>unknown</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_degreeOfEstablishment"></a>Term Name  dwc:degreeOfEstablishment</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/degreeOfEstablishment">http://rs.tdwg.org/dwc/terms/degreeOfEstablishment</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Degree of Establishment</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The degree to which an Organism survives, reproduces, and expands its range at the given place and time.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>Some preserved collections are specifically created from cultivated or captive organisms, or perhaps from rare vagrants.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to use controlled value strings from the controlled vocabulary designated for use with this term, listed at <a href="http://rs.tdwg.org/dwc/doc/doe/">http://rs.tdwg.org/dwc/doc/doe/</a>. For details, refer to <a href="https://doi.org/10.3897/biss.3.38084">https://doi.org/10.3897/biss.3.38084</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>native</code>, <code>captive</code>, <code>cultivated</code>, <code>released</code>, <code>failing</code>, <code>casual</code>, <code>reproducing</code>, <code>established</code>, <code>colonising</code>, <code>invasive</code>, <code>widespreadInvasive</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2020-10-13_27">http://rs.tdwg.org/decisions/decision-2020-10-13_27</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dc_description"></a>Term Name  dc:description</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://purl.org/dc/elements/1.1/description">http://purl.org/dc/elements/1.1/description</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Description</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An account of the resource.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A free text description or narrative about the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Use this field to record information about the collection in a human-readable, narrative style to introduce the main characteristics of the collection to someone unfamiliar to it. It may include additional information or re-state information held elsewhere in the collection description record - for example, for more atomic, categorised textual descriptions and narratives the MeasurementOrFact class should be used.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>The Chicago Academy of Sciences holds material documenting the biodiversity of Midwest / Western Great Lakes region from the 1830s to the present, and includes comparative and historic material collected across North America. These collections include zoology, botany, earth sciences, cultural, audiovisual, and archives. The institutional collection code CHAS was used historically to reference vertebrate and malacology collections at the Academy and was designated as the primary collection code for all the collections.</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_discipline"></a>Term Name  ltc:discipline</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/discipline">http://rs.tdwg.org/ltc/terms/discipline</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/discipline-2022-05-10">http://rs.tdwg.org/ltc/terms/version/discipline-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Discipline</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A high level classification of the scientific discipline to which the objects within the collection belong or are related.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The recommendation is to use a controlled vocabulary that is also common across other community collections, object and occurrence standards. Suggested list <a href="https://confluence.egi.eu/display/EGIG/Scientific+Disciplines">https://confluence.egi.eu/display/EGIG/Scientific+Disciplines</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Anthropology</code>, <code>Botany</code>, <code>Extraterrestrial</code>, <code>Geology</code>, <code>Microorganisms</code>, <code>Other geo/biodiversity</code>, <code>Palaeontology</code>, <code>Virology</code>, <code>Zoology invertebrates</code>, <code>Zoology vertebrates</code>, <code>Unspecified</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_knownToContainTypes"></a>Term Name  ltc:knownToContainTypes</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/knownToContainTypes">http://rs.tdwg.org/ltc/terms/knownToContainTypes</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/knownToContainTypes-2022-05-10">http://rs.tdwg.org/ltc/terms/version/knownToContainTypes-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Known To Contain Types</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Flag property to indicate that the collection is known to include type specimens.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>yes</code> <code>no</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_material"></a>Term Name  ltc:material</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/material">http://rs.tdwg.org/ltc/terms/material</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/material-2022-05-10">http://rs.tdwg.org/ltc/terms/version/material-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Material</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Material denotes the raw substance(s) from which the object is formed, in whole or in part.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This definition maps roughly to the concept of E57 'material' from the CIDOC CRM: <a href="https://cidoc-crm.org/Entity/E57-Material/version-7.1.1">https://cidoc-crm.org/Entity/E57-Material/version-7.1.1</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>The object, or artefact could contain biological parts, for example jewellery made of amber with insects in, or cloaks made of bird feathers. It should not be used for taxonomic identifications. Examples include terms such as <code>brick</code>, <code>gold</code>, <code>aluminium</code>, <code>polycarbonate</code>, <code>resin</code>, <code>amber</code>, <code>feather</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_objectType"></a>Term Name  ltc:objectType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/objectType">http://rs.tdwg.org/ltc/terms/objectType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/objectType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/objectType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Object Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>High-level terms for the classification of curated objects.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A more generic classification of items in the collection than described in preparationType.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This should not be used for classifying objects by taxon. The best way to do that is to use the Taxon class (formal taxonomy and vernacular names) or ObjectClassification class (informal classification). For cultural collections terms such as 'bowl', 'textile' are appropriate at this level. For large collections of multiple types use pipe delimited lists.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>tissue</code>, <code>specimen</code>, <code>culture</code>, <code>rna</code>, <code>mineral</code>, <code>dna</code>, <code>environmental sample</code>, <code>HTS Library</code>, <code>other</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_period"></a>Term Name  ltc:period</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/period">http://rs.tdwg.org/ltc/terms/period</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/period-2022-05-10">http://rs.tdwg.org/ltc/terms/version/period-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Period</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Used to describe prehistoric or historic periods.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>Used to describe the prehistoric or historic period  from which objects in the collection originated.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Often used to describe prehistoric or historic periods, but also geopolitical units and activities of settlements are regarded as special cases of Period. However, there are no assumptions about the scale of the associated phenomena. In particular all events are seen as synthetic processes consisting of coherent phenomena. This property maps to the Period class of the CIDOC-CRM conceptual reference model (<a href="http://www.cidoc-crm.org/Entity/e4-period/version-7.1.1">http://www.cidoc-crm.org/Entity/e4-period/version-7.1.1</a>).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Neolithic Period</code>, <code>Ming Dynasty</code>, <code>McCarthy Era</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_preparationType"></a>Term Name  ltc:preparationType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/preparationType">http://rs.tdwg.org/ltc/terms/preparationType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/preparationType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/preparationType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Preparation Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A term used to classify or describe an object that indicates the actions that have been taken upon it and/or the processes it has been put through to prepare it for scientific use or study.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A more specific classification of items in the collection than described in objectType.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This can be the same as PreservationMethod (e.g. Bone), but is not always. This should not be used for classifying objects by taxon. The best way to do that is to use the Taxon class (formal taxonomy and vernacular names) or ObjectClassification class (informal classification). For large collections with multiple types use a pipe delimited list.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Bones</code>, <code>Eggs</code>, <code>Fossils</code>, <code>Gemstones</code>, <code>Lysate</code>, <code>Macrofossils</code>, <code>eDNA</code>, <code>Viable cells</code>, <code>Pollen</code>, <code>Muscle</code>, <code>Leaf</code>, <code>Blood</code>, <code>Known - witheld</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_preservationMethod"></a>Term Name  ltc:preservationMethod</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/preservationMethod">http://rs.tdwg.org/ltc/terms/preservationMethod</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/preservationMethod-2022-05-10">http://rs.tdwg.org/ltc/terms/version/preservationMethod-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Preservation Method</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A term used to classify or describe an object that indicates the primary or most recent action, measure or process that has been used in order to preserve the objects in the collection for long-term storage.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>For the purposes of a collection description preservationType should be used to describe the larger collection</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Not intended to be used as the fossilization method. Use preservationMode for that. This field is intended to be use where a collection has a single or prominent preservationMethod. If the collection has multiple preservationMethods then this should be expressed elsewhere, such as in ObjectQuantity. We recommend the Arctos PART_PRESERVATION vocabulary (<a href="https://arctos.database.museum/info/ctDocumentation.cfm?table=CTPART_PRESERVATION">https://arctos.database.museum/info/ctDocumentation.cfm?table=CTPART_PRESERVATION</a>). For herbarium sheets use 'dried_pressed'. If an alcohol collection uses mixed percentages use 'alcohol'.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>fluid_preserved</code>, <code>alcohol</code>, <code>formaldehyde</code>, <code>dried</code>, <code>dried_pinned</code>, <code>dried_pressed</code>, <code>mounted</code>, <code>microscope_slide</code>, <code>glycerin</code>, <code>gum_arabic</code>, <code>frozen</code>, <code>refrigerated</code>, <code>freeze_dried</code>, <code>mixed</code>, <code>no_treatment</code>, <code>known:withheld</code>, <code>unknown</code>, <code>papered/packaged</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_preservationMode"></a>Term Name  ltc:preservationMode</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/preservationMode">http://rs.tdwg.org/ltc/terms/preservationMode</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/preservationMode-2022-05-10">http://rs.tdwg.org/ltc/terms/version/preservationMode-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Preservation Mode</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The means by which a palaeontological specimen was preserved or created e.g. body, cast, mold, trace fossil, soft parts mineralised etc.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>Use to describe the preservation mode of a collection as a whole. (e.g. Amber collection)</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property is aligned with the concept of preservationMode (<a href="https://efg.geocase.eu/documentation/html/efg.html#element_PreservationMode_Link03032878">https://efg.geocase.eu/documentation/html/efg.html#element_PreservationMode_Link03032878</a>) in ABCD(EFG).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>adpression/compression</code>, <code>body</code>, <code>cast</code>, <code>charcoalification</code>, <code>coalified</code>, <code>concretion</code>, <code>dissolution traces</code>, <code>mold/impression</code>, <code>permineralised</code>, <code>recrystallised</code>, <code>soft parts</code>, <code>trace</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_typeOfCollection"></a>Term Name  ltc:typeOfCollection</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/typeOfCollection">http://rs.tdwg.org/ltc/terms/typeOfCollection</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/typeOfCollection-2022-05-10">http://rs.tdwg.org/ltc/terms/version/typeOfCollection-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Type Of Collection</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Additional information that exists that describes the object(s) in the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Terms such as soil, pollen, faeces, muscle, genomic DNA are currently put in preparationType. These terms have been parked for discussion: HumanObservations, MachineObservations.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>PreservedSpecimens</code>, <code>FossilSpecimens</code>, <code>MineralSpecimens</code>, <code>ArchaeologicalArtefacts</code>, <code>EthnographicObjects</code>, <code>HumanRemains</code>, <code>HominidRemains</code>, <code>MaterialSamples</code>, <code>LivingSpecimens</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.13 Organisational Unit

A unit within an organisational hierarchy which may be at, above or below the institutional level. This class can represent any level of organisational unit, incorporating institutions (e.g. a museum), higher units (e.g. a university to which a museum belongs) and more detailed structures (e.g the departments and divisions within a museum). It can be used to arrange these different units at different levels into a hierarchical structure. Derived from [org:OrganizationalUnit](http://www.w3.org/ns/org#OrganizationalUnit) but is not exactly the same. This class combines aspects of both, class [org:Organization](https://www.w3.org/TR/2014/REC-vocab-org-20140116/#org:Organization) and class [org:OrganizationalUnit](https://www.w3.org/TR/2014/REC-vocab-org-20140116/#org:OrganizationalUnit) from the [W3C Organization Ontology ORG](https://www.w3.org/TR/2014/REC-vocab-org-20140116/#overview-of-ontology). Recommended best practice is to associate a unique, persistent organizational identifier (PID) with each created organizational unit. This will allow an unambiguous and continual identification of the unit, as well as the creation of organizational hierarchies. Existing providers of PIDs for organizations are, e.g. https://grid.ac/ and https://ror.org/. The provision of organizational PIDs might be extended to intra-organizational units in the future. Properties of Class: Identifier can be used to add identifier information for organizational units.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_OrganisationalUnit"></a>Term Name  ltc:OrganisationalUnit</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/OrganisationalUnit">http://rs.tdwg.org/ltc/terms/OrganisationalUnit</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/OrganisationalUnit-2022-05-10">http://rs.tdwg.org/ltc/terms/version/OrganisationalUnit-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Organisational Unit</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A unit within an organisational hierarchy which may be at, above or below the institutional level.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This class can represent any level of organisational unit, incorporating institutions (e.g. a museum), higher units (e.g. a university to which a museum belongs) and more detailed structures (e.g the departments and divisions within a museum). It can be used to arrange these different units at different levels into a hierarchical structure. This class combines aspects of both class org:Organization (<a href="https://www.w3.org/TR/2014/REC-vocab-org-20140116/#org:Organization">https://www.w3.org/TR/2014/REC-vocab-org-20140116/#org:Organization</a>) and class org:OrganizationalUnit (<a href="https://www.w3.org/TR/2014/REC-vocab-org-20140116/#org:OrganizationalUnit">https://www.w3.org/TR/2014/REC-vocab-org-20140116/#org:OrganizationalUnit</a>) from the W3C Organization Ontology ORG (<a href="https://www.w3.org/TR/2014/REC-vocab-org-20140116/#overview-of-ontology">https://www.w3.org/TR/2014/REC-vocab-org-20140116/#overview-of-ontology</a>). Recommended best practice is to associate a unique, persistent organizational identifier (PID) with each created organizational unit. This will allow an unambiguous and continual identification of the unit, as well as the creation of organizational hierarchies. Existing providers of PIDs for organizations are, e.g. <a href="https://grid.ac/">https://grid.ac/</a> and <a href="https://ror.org/">https://ror.org/</a>. The provision of organizational PIDs might be extended to intra-organizational units in the future. Properties of Class: Identifier can be used to add identifier information for organizational units.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_organisationalUnitName"></a>Term Name  ltc:organisationalUnitName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/organisationalUnitName">http://rs.tdwg.org/ltc/terms/organisationalUnitName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/organisationalUnitName-2022-05-10">http://rs.tdwg.org/ltc/terms/version/organisationalUnitName-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Organisational Unit Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An official name of the organisational unit in the local language.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Repeatable where there are more than one official local language required for example Belgian Institutions where an official name exists in French, Dutch, German and English. See 'A Collection of Crosswalks from Fifteen Research Data Schemas to Schema.org' (<a href="https://www.rd-alliance.org/group/research-metadata-schemas-wg/outcomes/collection-crosswalks-fifteen-research-data-schemas">https://www.rd-alliance.org/group/research-metadata-schemas-wg/outcomes/collection-crosswalks-fifteen-research-data-schemas</a>) from RDA for crosswalks for properties with the function of Name, Title, etc. Take into account the note at the class level (Class:OrganisationalUnit) about associating an identifier in addition to a name with the organizational unit.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Muséum national d'Histoire naturelle</code>, <code>The Field Museum of Natural History</code>, <code>Division of Fishes</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_organisationalUnitType"></a>Term Name  ltc:organisationalUnitType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/organisationalUnitType">http://rs.tdwg.org/ltc/terms/organisationalUnitType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/organisationalUnitType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/organisationalUnitType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Organisational Unit Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The type or level of organisational unit within a hierarchy responsible for the management of the collection being described.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Example vocabulary list: <a href="https://vocab.org/aiiso/">https://vocab.org/aiiso/</a> . This property is likely related to the W3C class org:Role (<a href="https://www.w3.org/TR/2014/REC-vocab-org-20140116/#class-role">https://www.w3.org/TR/2014/REC-vocab-org-20140116/#class-role</a>).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Department</code> (A group of people recognised by an organization as forming a cohesive group referred to by the organization as a department), <code>Division</code> (A group of people recognised by an organization as forming a cohesive group referred to by the organization as a division)</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.14 Person

A person (alive or dead). This concept should map to the Schema.org Person class (https://schema.org/Person), and the prov:Person class (http://www.w3.org/ns/prov#Person) in the PROV ontology. In the latter, it is a subclass of prov:Agent, which through which it can map to the RDA recommendations on attribution (http://dx.doi.org/10.15497/RDA00029). The definition is appropriated from the Schema.org class.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_Person"></a>Term Name  ltc:Person</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/Person">http://rs.tdwg.org/ltc/terms/Person</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/Person-2022-05-10">http://rs.tdwg.org/ltc/terms/version/Person-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Person</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A person (alive, dead, undead, or fictional).</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A person (alive or dead).</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This concept should map to the Schema.org Person class (<a href="https://schema.org/Person">https://schema.org/Person</a>), and the prov:Person class (<a href="http://www.w3.org/ns/prov#Person">http://www.w3.org/ns/prov#Person</a>) in the PROV ontology. In the latter, it is a subclass of prov:Agent, which through which it can map to the RDA recommendations on attribution (<a href="http://dx.doi.org/10.15497/RDA00029">http://dx.doi.org/10.15497/RDA00029</a>). The definition is appropriated from the Schema.org class.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_additionalName"></a>Term Name  schema:additionalName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/additionalName">https://schema.org/additionalName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Additional Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An additional name for a Person, can be used for a middle name.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Stewart</code>, <code>Grace</code>, <code>Manthey</code>, <code>Kwame</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_familyName"></a>Term Name  schema:familyName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/familyName">https://schema.org/familyName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Family Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Family name. In the U.S., the last name of a Person.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Jones</code>, <code>Keita</code>, <code>O'Rourke</code>, <code>Carreño Quiñones</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="abcd_fullName"></a>Term Name  abcd:fullName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/abcd/terms/fullName">http://rs.tdwg.org/abcd/terms/fullName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Full Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Preferred form of personal name for display as a string.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>James Ewert Bradshaw</code>, <code>T. van Hooijdonk</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="schema_givenName"></a>Term Name  schema:givenName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="https://schema.org/givenName">https://schema.org/givenName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Given Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Given name. In the U.S., the first name of a Person.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Beth</code>, <code>John</code>, <code>María José</code>, <code>Björn</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.15 Person Role

A qualified association between a Person or OrganisationalUnit and an entity such as an ObjectGroup or MeasurementOrFact that enables the relationship to be contextualised with a specific role and time period. This class is aligned with the prov:qualifiedAttribution property (http://www.w3.org/ns/prov#qualifiedAttribution). It should be used instead of the Activity and PersonActivity classes to link a Person or OrganisationalUnit to an entity in situations where an activity is not know or is irrelevant, for example for describing a person's role within an organisation.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_PersonRole"></a>Term Name  ltc:PersonRole</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/PersonRole">http://rs.tdwg.org/ltc/terms/PersonRole</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/PersonRole-2022-05-10">http://rs.tdwg.org/ltc/terms/version/PersonRole-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Person Role</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A qualified association between a Person or OrganisationalUnit and an entity such as an ObjectGroup or MeasurementOrFact that enables the relationship to be contextualised with a specific role and time period.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This class is aligned with the prov:qualifiedAttribution property (<a href="http://www.w3.org/ns/prov#qualifiedAttribution">http://www.w3.org/ns/prov#qualifiedAttribution</a>). It should be used instead of the Activity and PersonActivity classes to link a Person or OrganisationalUnit to an entity in situations where an activity is not know or is irrelevant, for example for describing a person's role within an organisation.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_endedAtTime"></a>Term Name  ltc:endedAtTime</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/endedAtTime">http://rs.tdwg.org/ltc/terms/endedAtTime</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/endedAtTime-2022-05-10">http://rs.tdwg.org/ltc/terms/version/endedAtTime-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Ended At Time</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The date or time when a Person stopped fulfilling the role specified in the role property.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property maps to the PROV-O term endedAtTime (<a href="http://www.w3.org/ns/prov#endedAtTime">http://www.w3.org/ns/prov#endedAtTime</a>) in the Activity class (<a href="http://www.w3.org/ns/prov#Activity">http://www.w3.org/ns/prov#Activity</a>).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>1886</code>, <code>1984-09</code>, <code>2001-10-22</code>, <code>1997-07-16T19:20+01:00</code>, <code>1997-07-16T19:20:30+01:00</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_role"></a>Term Name  ltc:role</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/role">http://rs.tdwg.org/ltc/terms/role</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/role-2022-05-10">http://rs.tdwg.org/ltc/terms/version/role-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Role</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A role played by a Person in the context of an entity such as an ObjectGroup, OrganisationalUnit or RecordLevel.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property maps to the PROV-O property hadRole (<a href="http://www.w3.org/ns/prov#hadRole">http://www.w3.org/ns/prov#hadRole</a>).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Director</code>, <code>Chair</code>, <code>Record owner</code>, <code>Primary Collection Description record contact</code>, <code>Primary collection contact</code>, <code>Owner</code>, <code>Curator</code>, <code>Collection manager</code>, <code>Head of department</code>, <code>Registrar</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_startedAtTime"></a>Term Name  ltc:startedAtTime</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/startedAtTime">http://rs.tdwg.org/ltc/terms/startedAtTime</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/startedAtTime-2022-05-10">http://rs.tdwg.org/ltc/terms/version/startedAtTime-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Started At Time</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The date or time when a Person started fulfilling the role specified in the role property.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property maps to the PROV-O term startedAtTime (<a href="http://www.w3.org/ns/prov#startedAtTime">http://www.w3.org/ns/prov#startedAtTime</a>) in the Activity class (<a href="http://www.w3.org/ns/prov#Activity">http://www.w3.org/ns/prov#Activity</a>).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>1886</code>, <code>1984-09</code>, <code>2001-10-22</code>, <code>1997-07-16T19:20+01:00</code>, <code>1997-07-16T19:20:30+01:00</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.16 Record Level

The machine-actionable information profile for the collection description digital object. Linked to the RDA PID Kernel recommendation (https://www.rd-alliance.org/system/files/RDA%20Recommendation%20on%20PID%20Kernel%20Information_final.pdf)<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_RecordLevel"></a>Term Name  ltc:RecordLevel</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/RecordLevel">http://rs.tdwg.org/ltc/terms/RecordLevel</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/RecordLevel-2022-05-10">http://rs.tdwg.org/ltc/terms/version/RecordLevel-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Record Level</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The machine-actionable information profile for the collection description digital object.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Linked to the RDA PID Kernel recommendation (<a href="https://www.rd-alliance.org/system/files/RDA%20Recommendation%20on%20PID%20Kernel%20Information_final.pdf">https://www.rd-alliance.org/system/files/RDA%20Recommendation%20on%20PID%20Kernel%20Information_final.pdf</a>)</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_collectionDescriptionPID"></a>Term Name  ltc:collectionDescriptionPID</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/collectionDescriptionPID">http://rs.tdwg.org/ltc/terms/collectionDescriptionPID</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/collectionDescriptionPID-2022-05-10">http://rs.tdwg.org/ltc/terms/version/collectionDescriptionPID-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Collection Description PID</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An unambiguous reference to the collection description record.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended practice is to identify the resource by means of a string conforming to an identification system. Examples include International Standard Book Number (ISBN), Digital Object Identifier (DOI), and Uniform Resource Name (URN). Persistent identifiers should be provided as HTTP URIs.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>10.5072/example-full</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_derivedCollection"></a>Term Name  ltc:derivedCollection</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/derivedCollection">http://rs.tdwg.org/ltc/terms/derivedCollection</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/derivedCollection-2022-05-10">http://rs.tdwg.org/ltc/terms/version/derivedCollection-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Derived Collection</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A flag to indicate that the collection description has been generated by aggregating data from one or more underlying datasets of its individual objects.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>For example this would be set = Yes if the record is an automatically generated reconstruction of Darwin's finch collection which is now held at multiple institutions.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Yes</code>, <code>No</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dc_license"></a>Term Name  dc:license</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://purl.org/dc/elements/1.1/license">http://purl.org/dc/elements/1.1/license</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>License</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A legal document giving official permission to do something with the resource.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A legal document giving official permission to do something with the collection description record.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended practice is to identify the license document with a URI. If this is not possible or feasible, a literal value that identifies the license may be provided.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code><a href="https://creativecommons.org/licenses/by/4.0/">https://creativecommons.org/licenses/by/4.0/</a></code>, <code><a href="https://creativecommons.org/publicdomain/zero/1.0/">https://creativecommons.org/publicdomain/zero/1.0/</a></code>, <code><a href="https://creativecommons.org/licenses/by/4.0/legalcode">https://creativecommons.org/licenses/by/4.0/legalcode</a></code>, <code><a href="https://opendatacommons.org/licenses/by/1.0/">https://opendatacommons.org/licenses/by/1.0/</a></code>, <code><a href="http://unlicense.org/">http://unlicense.org/</a></code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dc_recordRights"></a>Term Name  dc:recordRights</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://purl.org/dc/elements/1.1/recordRights">http://purl.org/dc/elements/1.1/recordRights</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Record Rights</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Information about rights held in and over the resource.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A statement of any rights held in/over the collection description record.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Typically, rights information includes a statement about various property rights associated with the resource, including intellectual property rights. Recommended practice is to refer to a rights statement with a URI. If this is not possible or feasible, a literal value (name, label, or short text) may be provided.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code><a href="http://scratchpads.eu/about/policies/termsandconditions">http://scratchpads.eu/about/policies/termsandconditions</a></code>, <code>All rights reserved by DataOwner Ltd.</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dc_rightsHolder"></a>Term Name  dc:rightsHolder</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://purl.org/dc/elements/1.1/rightsHolder">http://purl.org/dc/elements/1.1/rightsHolder</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Rights Holder</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A person or organization owning or managing rights over the resource.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A person or organization owning or managing rights held in/over the collection description record.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended practice is to refer to the rights holder with a URI. If this is not possible or feasible, a literal value that identifies the rights holder may be provided.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Smith, Clare</code>, <code>Natural History Museum, London</code>, <code><a href="https://orcid.org/XXXX-XXXX-XXXX-XXXX">https://orcid.org/XXXX-XXXX-XXXX-XXXX</a></code>, <code><a href="https://ror.org/XXaaaXXXX">https://ror.org/XXaaaXXXX</a></code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.17 Reference

A reference to external resources and information related to the collection description. In the Collection Description standard, this class can be used to store references to publications, policies, datasets and other online resources such as websites, related to classes within the standard.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_Reference"></a>Term Name  dwc:Reference</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/Reference">http://rs.tdwg.org/dwc/terms/Reference</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Reference</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A class to describe a scientific reference or citation.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A reference to external resources and information related to the collection description.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>In the Collection Description standard, this class can be used to store references to publications, policies, datasets and other online resources such as websites, related to classes within the standard.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="abcd_referenceDetails"></a>Term Name  abcd:referenceDetails</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/abcd/terms/referenceDetails">http://rs.tdwg.org/abcd/terms/referenceDetails</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Reference Details</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Detailed information related to a class.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>Detailed information about the resource being referenced.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>This dataset includes a Darwin Core Archive of the ~8000 specimens digitised to date, of which ~80% also have an associated label image.</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="abcd_referenceText"></a>Term Name  abcd:referenceText</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/abcd/terms/referenceText">http://rs.tdwg.org/abcd/terms/referenceText</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Reference Text</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A generic text property to describe a class.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A short title for the reference.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Digitised specimen records on the NHM Data Portal</code>, <code>BGBM loans policy</code>, <code>Herbarium Wikipedia page</code>, <code>NMNH website</code>, <code>Related sequences in GenBank</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_referenceType"></a>Term Name  ltc:referenceType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/referenceType">http://rs.tdwg.org/ltc/terms/referenceType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/referenceType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/referenceType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Reference Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The type of resource being referenced.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property is intended to be used for a high level categorisation of resource types.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Policy</code>, <code>Document</code>, <code>Website</code>, <code>Dataset</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="abcd_resourceURI"></a>Term Name  abcd:resourceURI</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/abcd/terms/resourceURI">http://rs.tdwg.org/abcd/terms/resourceURI</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Resource URI</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A preferably resolvable URI to uniquely identify a concept.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A preferably resolvable URI providing access to the resource defined in the reference.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>10.5072/example-full</code>, <code><a href="https://examplemuseum.org/policies/loans-policy.pdf">https://examplemuseum.org/policies/loans-policy.pdf</a></code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.18 Resource Relationship

A relationship between an instance of a class in the collection description standard to another instance of the same class, or an instance of a different class in the standard. In the context of this standard, the resources are the collections of objects represented by the ObjectGroup. This class can be used to define different semantic and hierarchical relationships between ObjectGroups.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_ResourceRelationship"></a>Term Name  dwc:ResourceRelationship</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/ResourceRelationship">http://rs.tdwg.org/dwc/terms/ResourceRelationship</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Resource Relationship</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A relationship of one rdfs:Resource (http://www.w3.org/2000/01/rdf-schema#Resource) to another.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>A relationship between an instance of a class in the collection description standard to another instance of the same class, or an instance of a different class in the standard.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>In the context of this standard, the resources are the collections of objects represented by the ObjectGroup. This class can be used to define different semantic and hierarchical relationships between ObjectGroups.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2014-10-26_15">http://rs.tdwg.org/decisions/decision-2014-10-26_15</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_relatedResourceID"></a>Term Name  dwc:relatedResourceID</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/relatedResourceID">http://rs.tdwg.org/dwc/terms/relatedResourceID</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Related Resource ID</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An identifier for a related resource (the object, rather than the subject of the relationship).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>dc609808-b09b-11e8-96f8-529269fb1459</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_relatedResourceName"></a>Term Name  ltc:relatedResourceName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/relatedResourceName">http://rs.tdwg.org/ltc/terms/relatedResourceName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/relatedResourceName-2022-05-10">http://rs.tdwg.org/ltc/terms/version/relatedResourceName-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Related Resource Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A short textual name for the related resource.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property can be used to list resources related to the source entity which lack an identifier, for example if a separate record for that resource doesn't yet exist. In the Collection Description standard, a use of this is to list named subcollections of a larger collections at a time when the resources might not be available to create a full Collection Description for each of them. If at a later point a Collection Description record is created for the subcollection, an identifier can be added to the relatedResourceID property to maintain the same relationship.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>FMNH Mammals</code>, <code>TNHC Vertebrates</code>, <code>Sloane Herbarium</code>, <code>Grant Southwest Ceramics Collection</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_relationshipAccordingTo"></a>Term Name  dwc:relationshipAccordingTo</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/relationshipAccordingTo">http://rs.tdwg.org/dwc/terms/relationshipAccordingTo</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Relationship According To</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The source (person, organization, publication, reference) establishing the relationship between the two resources.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Julie Woodruff</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_relationshipEstablishedDate"></a>Term Name  dwc:relationshipEstablishedDate</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/relationshipEstablishedDate">http://rs.tdwg.org/dwc/terms/relationshipEstablishedDate</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Relationship Established Date</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The date-time on which the relationship between the two resources was established.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to use a date that conforms to ISO 8601-1:2019.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>1963-03-08T14:07-0600</code>, <code>2009-02-20T08:40Z</code>, <code>2018-08-29T15:19</code>, <code>1809-02-12</code>, <code>1906-06</code>, <code>1971</code>, <code>2007-03-01T13:00:00Z/2008-05-11T15:30:00Z</code>, <code>1900/1909</code>, <code>2007-11-13/15</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_relationshipOfResource"></a>Term Name  dwc:relationshipOfResource</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/relationshipOfResource">http://rs.tdwg.org/dwc/terms/relationshipOfResource</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Relationship Of Resource</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The relationship of the resource identified by relatedResourceID to the subject (optionally identified by the resourceID).</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to use a controlled vocabulary. <a href="https://schema.org/Property">https://schema.org/Property</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>part of</code>, <code>contains</code>, <code>same as</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_relationshipRemarks"></a>Term Name  dwc:relationshipRemarks</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/relationshipRemarks">http://rs.tdwg.org/dwc/terms/relationshipRemarks</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Relationship Remarks</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Comments or notes about the relationship between the two resources.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>The Darwin fossil collection makes up part of the museum's palaeontology collection.</code>, <code>Some of the same Madagascan bryophytes are included in both of these collections.</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_resourceID"></a>Term Name  dwc:resourceID</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/resourceID">http://rs.tdwg.org/dwc/terms/resourceID</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Resource ID</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An identifier for the resource that is the subject of the relationship.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>f809b9e0-b09b-11e8-96f8-529269fb1459</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_resourceRelationshipID"></a>Term Name  dwc:resourceRelationshipID</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/resourceRelationshipID">http://rs.tdwg.org/dwc/terms/resourceRelationshipID</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Resource Relationship ID</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An identifier for an instance of relationship between one resource (the subject) and another (relatedResource, the object).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>04b16710-b09c-11e8-96f8-529269fb1459</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.19 Scheme Measurement Or Fact

A type of measurement or fact used by the CollectionDescriptionScheme, and the rules relating to its application. This class can be used to specify the qualitative and quantitative metrics that will be included in the CollectionDescriptionScheme using the MeasurementOrFact class, and dictate whether each will be mandatory and/or repeatable. This information can be used by software and queries to constrain and validate the Latimer Core dataset, and determine how and whether metrics can be aggregated and reported. The schemeMeasurementType property should correspond to the measurementType property of the MeasurementOrFact class in order to make the relevant association between the scheme definition and the stored data.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_SchemeMeasurementOrFact"></a>Term Name  ltc:SchemeMeasurementOrFact</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/SchemeMeasurementOrFact">http://rs.tdwg.org/ltc/terms/SchemeMeasurementOrFact</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/SchemeMeasurementOrFact-2022-05-10">http://rs.tdwg.org/ltc/terms/version/SchemeMeasurementOrFact-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Scheme Measurement Or Fact</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A type of measurement or fact used by the CollectionDescriptionScheme, and the rules relating to its application.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This class can be used to specify the qualitative and quantitative metrics that will be included in the CollectionDescriptionScheme using the MeasurementOrFact class, and dictate whether each will be mandatory and/or repeatable. This information can be used by software and queries to constrain and validate the Latimer Core dataset, and determine how and whether metrics can be aggregated and reported. The schemeMeasurementType property should correspond to the measurementType property of the MeasurementOrFact class in order to make the relevant association between the scheme definition and the stored data.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_mandatoryMetric"></a>Term Name  ltc:mandatoryMetric</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/mandatoryMetric">http://rs.tdwg.org/ltc/terms/mandatoryMetric</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/mandatoryMetric-2022-05-10">http://rs.tdwg.org/ltc/terms/version/mandatoryMetric-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Mandatory Metric</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A flag to designate whether it's mandatory or optional for every collection description within the CollectionDescriptionScheme to include the measurement or fact defined by the schemeMeasurementType property.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This flag can be used for software automation and data validation.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>true</code>, <code>false</code>, <code>yes</code>, <code>no</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_repeatableMetric"></a>Term Name  ltc:repeatableMetric</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/repeatableMetric">http://rs.tdwg.org/ltc/terms/repeatableMetric</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/repeatableMetric-2022-05-10">http://rs.tdwg.org/ltc/terms/version/repeatableMetric-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Repeatable Metric</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A flag to designate whether multiple instances of the same schemeMeasurementType may be attached to a single entity.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>For example, this property can be used to stipulate that, using the MeasurementOrFact class, only one 'Object count' may be attached to an ObjectGroup, but multiple 'Curator notes' may be attached to the same ObjectGroup.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>true</code>, <code>false</code>, <code>yes</code>, <code>no</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_schemeMeasurementType"></a>Term Name  ltc:schemeMeasurementType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/schemeMeasurementType">http://rs.tdwg.org/ltc/terms/schemeMeasurementType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/schemeMeasurementType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/schemeMeasurementType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Scheme Measurement Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A category of quantitative metric or qualitative fact that can be included in the CollectionDescriptionScheme.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The schemeMeasurementType should correspond to, and be used to catalogue and/or constrain, the values that can be used in the measurementType property of the MeasurementOrFact class.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Imaged Level Percentage</code>, <code>Storage Volume</code>, <code>Object Count</code>, <code>MIDS-0 Object Count</code>, <code>Historical Narrative</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.20 Scheme Term

A Latimer Core term used by the CollectionDescriptionScheme and the rules relating to its application. This class can be used to define which of the terms (classes and/or properties) within the standard (e.g. GeographicOrigin, Taxon, preservationMethod) are expected to be used within the scheme, and specify whether they're mandatory and/or repeatable. This information can be used by software and queries to validate the data and understand the rules by which metrics can be reported against the specified term.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_SchemeTerm"></a>Term Name  ltc:SchemeTerm</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/SchemeTerm">http://rs.tdwg.org/ltc/terms/SchemeTerm</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/SchemeTerm-2022-05-10">http://rs.tdwg.org/ltc/terms/version/SchemeTerm-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Scheme Term</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A Latimer Core term used by the CollectionDescriptionScheme and the rules relating to its application.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This class can be used to define which of the terms (classes and/or properties) within the standard (e.g. GeographicOrigin, Taxon, preservationMethod) are expected to be used within the scheme, and specify whether they're mandatory and/or repeatable. This information can be used by software and queries to validate the data and understand the rules by which metrics can be reported against the specified term.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_mandatoryTerm"></a>Term Name  ltc:mandatoryTerm</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/mandatoryTerm">http://rs.tdwg.org/ltc/terms/mandatoryTerm</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/mandatoryTerm-2022-05-10">http://rs.tdwg.org/ltc/terms/version/mandatoryTerm-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Mandatory Term</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A flag to designate whether it's mandatory or optional for all ObjectGroups in the CollectionDescriptionScheme to include or be linked to valid data for the class or property defined in the termName property.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This flag can be used for software automation and data validation. For example, if the termName is 'preservationMethod' (a property) and mandatoryTerm is 'yes', then an interface or query should always expect a value for that property, and can validate against that expectation. If the termName is Taxon (a class) and the mandatoryTerm is 'yes', then similarly the expectation will be that at least one populated Taxon object is linked to every ObjectGroup. If the repeatableTerm property is set to 'no', then the expectation will be that exactly one populated Taxon object is linked to every ObjectGroup and no more.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>true</code>, <code>false</code>, <code>yes</code>, <code>no</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_repeatableTerm"></a>Term Name  ltc:repeatableTerm</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/repeatableTerm">http://rs.tdwg.org/ltc/terms/repeatableTerm</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/repeatableTerm-2022-05-10">http://rs.tdwg.org/ltc/terms/version/repeatableTerm-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Repeatable Term</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A flag to designate whether multiple instances of the Latimer Core class or property defined in the termName property may be attached to a single ObjectGroup.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This property essentially defines whether the property or class is used for a 'tagging' approach (e.g. attaching multiple Taxon records to the same ObjectGroup to reflect the taxonomic scope, or a 'dimensional' approach (e.g. attaching a single GeologicalContext to an ObjectGroup, to show that it represents only objects from the Mesozoic). This has implications on how metrics may be handled, and more information is available in the non-normative guidance.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>true</code>, <code>false</code>, <code>yes</code>, <code>no</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_termName"></a>Term Name  ltc:termName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/termName">http://rs.tdwg.org/ltc/terms/termName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/termName-2022-05-10">http://rs.tdwg.org/ltc/terms/version/termName-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Term Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The name of a class or property within the Latimer Core standard that is included in the CollectionDescriptionScheme.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The values of this property are constrained to the names of terms (classes or properties) within the Latimer Core standard.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>GeographicOrigin</code>, <code>Taxon</code>, <code>preservationMethod</code>, <code>discipline</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.21 Storage Location

A physical location (such as a building, room, cabinet or drawer) within the holding institution where objects associated with the collection description are stored or exhibited.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_StorageLocation"></a>Term Name  ltc:StorageLocation</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/StorageLocation">http://rs.tdwg.org/ltc/terms/StorageLocation</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/StorageLocation-2022-05-10">http://rs.tdwg.org/ltc/terms/version/StorageLocation-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Storage Location</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A physical location (such as a building, room, cabinet or drawer) within the holding institution where objects associated with the collection description are stored or exhibited.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_locationName"></a>Term Name  ltc:locationName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/locationName">http://rs.tdwg.org/ltc/terms/locationName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/locationName-2022-05-10">http://rs.tdwg.org/ltc/terms/version/locationName-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Location Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A label used to identify a place where the collection is stored.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This is the lowest level of storage location for the object group (collection or sub-collection).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Building A</code>, <code>Cryptogamic herbarium</code>, <code>Cupboard C1</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_locationType"></a>Term Name  ltc:locationType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/locationType">http://rs.tdwg.org/ltc/terms/locationType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/locationType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/locationType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Location Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The nature of the location where the collection is stored.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This defines the type of storage location named in locationName, and may refer to static locations or moveable containers.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Site</code>, <code>Building</code>, <code>Floor</code>, <code>Room</code>, <code>Cabinet</code>, <code>Drawer</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.22 Taxon

A group of organisms (sensu http://purl.obolibrary.org/obo/OBI_0100026) considered by taxonomists to form a homogeneous unit.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_Taxon"></a>Term Name  dwc:Taxon</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/Taxon">http://rs.tdwg.org/dwc/terms/Taxon</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Taxon</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A group of organisms (sensu http://purl.obolibrary.org/obo/OBI_0100026) considered by taxonomists to form a homogeneous unit.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2014-10-26_15">http://rs.tdwg.org/decisions/decision-2014-10-26_15</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_genus"></a>Term Name  dwc:genus</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/genus">http://rs.tdwg.org/dwc/terms/genus</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Genus</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full scientific name of the genus in which the taxon is classified.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full scientific name of the genus in which the collection's taxa are classified.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Puma</code>, <code>Monoclea</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_kingdom"></a>Term Name  dwc:kingdom</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/kingdom">http://rs.tdwg.org/dwc/terms/kingdom</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Kingdom</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full scientific name of the kingdom in which the taxon is classified.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full scientific name of the kingdom in which the taxa in the collection are classified.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Other examples of controlled vocabularies <a href="http://tdwg.github.io/ontology/ontology/voc/Collection.rdf">http://tdwg.github.io/ontology/ontology/voc/Collection.rdf</a>   <a href="https://doi.org/10.1371/journal.pone.0130114">https://doi.org/10.1371/journal.pone.0130114</a> <a href="https://en.wikipedia.org/wiki/Two-empire_system">https://en.wikipedia.org/wiki/Two-empire_system</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Animalia</code>, <code>Archaea</code>, <code>Bacteria</code>, <code>Chromista</code>, <code>Fungi</code>, <code>Plantae</code>, <code>Protozoa</code>, <code>Viruses</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_scientificName"></a>Term Name  dwc:scientificName</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/scientificName">http://rs.tdwg.org/dwc/terms/scientificName</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Scientific Name</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The full scientific name, with authorship and date information if known. When forming part of an Identification, this should be the name in lowest level taxonomic rank that can be determined. This term should not contain identification qualifications, which should instead be supplied in the IdentificationQualifier term.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>The full scientific name. This should be the name in lowest level taxonomic rank that applies across the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>If this field is used, then recommended to also complete the taxonRank. This term should not contain identification qualifications.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Coleoptera</code> (order), <code>Vespertilionidae</code> (family), <code>Manis</code> (genus), <code>Ctenomys sociabilis</code> (genus + specificEpithet), <code>Ambystoma tigrinum diaboli</code> (genus + specificEpithet + infraspecificEpithet)</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
		<tr>
			<td>Executive Committee decision</td>
			<td><a href="http://rs.tdwg.org/decisions/decision-2019-12-01_19">http://rs.tdwg.org/decisions/decision-2019-12-01_19</a></td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="dwc_taxonRank"></a>Term Name  dwc:taxonRank</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/dwc/terms/taxonRank">http://rs.tdwg.org/dwc/terms/taxonRank</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Taxon Rank</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The taxonomic rank of the most specific name in the scientificName.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to use a controlled vocabulary. For example: <a href="https://bioportal.bioontology.org/ontologies/TAXRANK?p=summary">https://bioportal.bioontology.org/ontologies/TAXRANK?p=summary</a></td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>subspecies</code>, <code>varietas</code>, <code>forma</code>, <code>species</code>, <code>genus</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


### 4.23 Temporal Coverage

A record of a time range represented by the collection's establishment or change over time. This term is separate from the living or geologic periods represented by the objects in the collection. This class can be used to reflect temporal coverage of the collection within various contexts (defined by the temporalCoverageType property). Examples might include the time range in which objects within the collection were collected or the time period over which the collection was assembled.  It should not be used to document the time range within which the objects in the collection were alive, and if the time period you are trying to describe is better described by the CollectionHistory, GeologicalContext or ChronometricAge classes, or period property of the ObjectGroup class, then those classes or properties should be used instead. For example, the period property of the ObjectGroup class and/or GeologicalContext class should be used to record named time periods.<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_TemporalCoverage"></a>Term Name  ltc:TemporalCoverage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/TemporalCoverage">http://rs.tdwg.org/ltc/terms/TemporalCoverage</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/TemporalCoverage-2022-05-10">http://rs.tdwg.org/ltc/terms/version/TemporalCoverage-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Temporal Coverage</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A record of a time range represented by the collection's establishment or change over time. This term is separate from the living or geologic periods represented by the objects in the collection.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This class can be used to reflect temporal coverage of the collection within various contexts (defined by the temporalCoverageType property). Examples might include the time range in which objects within the collection were collected or the time period over which the collection was assembled.  It should not be used to document the time range within which the objects in the collection were alive, and if the time period you are trying to describe is better described by the CollectionHistory, GeologicalContext or ChronometricAge classes, or period property of the ObjectGroup class, then those classes or properties should be used instead. For example, the period property of the ObjectGroup class and/or GeologicalContext class should be used to record named time periods.</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Class</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_temporalCoverageEndDate"></a>Term Name  ltc:temporalCoverageEndDate</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/temporalCoverageEndDate">http://rs.tdwg.org/ltc/terms/temporalCoverageEndDate</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/temporalCoverageEndDate-2022-05-10">http://rs.tdwg.org/ltc/terms/version/temporalCoverageEndDate-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Temporal Coverage End Date</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>End date of the time range of the collection.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>If there is a temporalCoverageStartDate value and the action being documented is ongoing temporalCoverageEndDate should remain NULL, otherwise temporalCoverageEndDate = temporalCoverageStartDate.  If there is a temporalCoverageEndDate value, temporalCoverageType is strongly recommended.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>1886</code>, <code>1984-09</code>, <code>2001-10-22</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_temporalCoverageStartDate"></a>Term Name  ltc:temporalCoverageStartDate</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/temporalCoverageStartDate">http://rs.tdwg.org/ltc/terms/temporalCoverageStartDate</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/temporalCoverageStartDate-2022-05-10">http://rs.tdwg.org/ltc/terms/version/temporalCoverageStartDate-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Temporal Coverage Start Date</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Start date of the time range of the collection.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>If there is a temporalCoverageStartDate value, temporalCoverageType is recommended.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>1886</code>, <code>1984-09</code>, <code>2001-10-22</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2"><a id="ltc_temporalCoverageType"></a>Term Name  ltc:temporalCoverageType</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/temporalCoverageType">http://rs.tdwg.org/ltc/terms/temporalCoverageType</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2022-05-10</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/ltc/terms/version/temporalCoverageType-2022-05-10">http://rs.tdwg.org/ltc/terms/version/temporalCoverageType-2022-05-10</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Temporal Coverage Type</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The type or context of the time range associated with the collection's establishment. Separate from the living or geologic periods represented by the objects in the collection.</td>
		</tr>
		<tr>
			<td>Usage</td>
			<td>If there is a value for temporalCoverageStartDate or temporalCoverageEndDate, temporalCoverageType is recommended.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommendation is to use a controlled vocabulary.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td><code>Collecting time range</code> <code>Establishment time range</code></td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


