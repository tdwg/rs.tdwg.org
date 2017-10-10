# TDWG Standards Metadata

This repo contains the source CSV files containing the metadata necessary to generate RDF and HTML representations of the various components of Biodiversity Information Standards (TDWG) standards in accordance with the TDWG Standards Documentation Specification.

## 1 Metadata model for TDWG standards

![](https://raw.githubusercontent.com/tdwg/vocab/master/tdwg-standards-hierarchy-2017-01-23.png)
Fig. 1. TDWG Standards hierarchy model (image from [Standards Documentation Standard GitHub repository](https://github.com/tdwg/vocab/blob/master/hierarchy-model.md))

The TDWG Standards Documentation Specification (http://www.tdwg.org/standards/147) defines a hierarchical model for components of TDWG Standards (Fig. 1).  At the highest level (1st level) are Standards.  All TDWG Standards are linked by virtue of a common publisher relationship with TDWG itself.  Documents and Vocabularies (2nd level) are the parts of Standards.  Vocabularies are composed of Term Lists (3rd level), which correspond roughly to namespaces that define sets of terms.  The Term Lists are composed of Terms (4th level), which may be Properties, Classes, or Concepts.  

Each of the levels in the standards hierarchy are linked to the level above by a isPartOf relationsip, and to the level below by a hasPart relationship.  

![](https://github.com/tdwg/vocab/raw/master/graphics/version-model.png)
Fig. 2. Version model used to describe standards-related resources (image from the [Standards Documentation Specification](https://github.com/tdwg/vocab/blob/master/sds/documentation-specification.md))

Any resource in the hierarchy above can be considered to consist of an abstract resource that persists over time, referred to as a "current resource".  In Fig. 2, the arrow represents a current resource named *ex:resource*.  A current resource has a creation date, and a last modified date.

The state of current resources over time is documented by versions of that resource.  The versions are "snapshots" of the resource at a particular instant in time.  In Fig. 2, the vertical lines represent versions, for example the version named *ex:resource-2009-07-18*.  

The state of most properties of a current resource at the present time are shared by the most recent version of that resource. The properties of a current resource may change when a new version is issued.  The issued date of the new version becomes the modified date of the current resource.

A current resource is related to each of its versions by a hasVersion relationship.  A version of a resource is related to its current resource by an isVersionOf relationship.  A version is related to a previous version by a replaces relationship and to a subsequent version by an isReplacedBy relationship.  

## 2 IRI patterns

### 2.1 Patterns for current resources in the standards hierarchy

The IRI repsenting TDWG as an orgainzation is:

```
https://www.grid.ac/institutes/grid.480498.9
```

**1st level:** IRIs representing TDWG standards are in the form:

```
http://www.tdwg.org/standards/nnn
```

where "nnn" is a number unique to a particular standard.

**2nd level:** IRIs representing vocabularies are in the form:

```
http://rs.tdwg.org/vvv/
```

where "vvv" is a string unique to the vocabulary.  For example, "dwc" is the string for the basic Darwin Core vocabulary and "ac" is the string for the Audubon Core vocabulary.

**3rd level** IRIs representing term lists are in the form:

```
http://rs.tdwg.org/vvv/sss/
```

where "sss" is a string representing the term list that is unique within vocabulary "vvv".  IRI examples are:

```
http://rs.tdwg.org/dwc/iri/
```
for Darwin Core IRI-value Terms and

```
http://rs.tdwg.org/ac/terms/
```
for terms defined by Audubon Core.

**4th level** IRIs representing vocabulary terms are in the form:

```
http://rs.tdwg.org/vvv/sss/ttt
```

where "ttt" is the local name of a term defined as part of the term list ```http://rs.tdwg.org/vvv/sss/```.  IRI examples are:  

```
http://rs.tdwg.org/dwc/iri/recordedBy
http://rs.tdwg.org/dwc/ac/caption
```

Term IRIs are not followed by a trailing forward slash.  The "namespace" corresponding to the defining term list can be abbreviated to form a compact IRI ([CURIE](https://www.w3.org/TR/curie/)).  Since dwciri: abbreviates ```http://rs.tdwg.org/dwc/iri/``` and ac: abbreviates ```http://rs.tdwg.org/dwc/ac/```, the two term IRIs given as examples above can be expressed as the CURIEs ```dwciri:recordedBy``` and ```ac:caption```.

### 2.2 patterns for versions of resources in the standards hierarchy

**1st level:** Standards

A standard with IRI in the form

```
http://www.tdwg.org/standards/nnn
```

has versions with IRIs in the form

```
http://www.tdwg.org/standards/nnn/version/yyyy-mm-dd
```

where yyyy-mm-dd represents the issued date of the version, using the [lexical space of an XML schema date datatype](https://www.w3.org/TR/xmlschema-2/#date) (without timezone indicator).

**2nd level:** Vocabularies

A vocabulary with IRI in the form

```
http://rs.tdwg.org/vvv/
```

has versions with IRIs in the form

```
http://rs.tdwg.org/version/vvv/yyyy-mm-dd
```
with yyyy-mm-dd as described for standards.

**3rd level:** Term Lists

A term list with IRI in the form

```
http://rs.tdwg.org/vvv/sss/
```

has versions with IRIs in the form

```
http://rs.tdwg.org/vvv/version/sss/yyyy-mm-dd
```

**4th level:** Terms

A term with IRI in the form

```
http://rs.tdwg.org/vvv/sss/ttt
```

has versions with IRIs in the form

```
http://rs.tdwg.org/vvv/sss/version/ttt-yyyy-mm-dd
```


## 3 About directories in this repository

### 3.1 Relationship of parts of this repository to the metadata model

Each directory in this repository contain metadata for a group of resources at some level in the hierarchy.

Directories whose names do not end in "-versions" contain metadata about current resources.  Directory names ending in "-versions" contain metadata for versions of the current resources described in the corresponding folders that do not end in "-versions".

### 3.2 Files contained in current resources directories

Within each current resource directory there is a file whose name corresponds to the containing directory, plus the ".csv" file extension.  That file contains the primary metadata about the resources described in that folder.  For example, in the ```terms``` directory, the file ```terms.csv``` is the primary metadata file.  The corresponding file with name ending in "-column-mappings.csv" maps the columns in the primary metadata file to standard metadata properties (similar in function to the meta.xml file of a Darwin Core Archive).  Example: ```terms-column-mappings.csv```.  

The current resource directory also contains two files that contain link tables that describe one-to-many relationships between the current resource and related resources.  The file with name ending in "-replacements.csv" (example: ```terms-replacements.csv```) links current resources to other current resources that replace them.  The file with name ending in "-versions.csv" (example: ```terms-versions.csv```) links versions to their corresponding current term.

There are other files in each directory that contain configuration information or other information necessary to generate the machine readable metadata for the resources described in that directory.

### 3.3 Files contained in versions directories

Within each folder describing versions, the primary metadata is in the file whose name corresponds to the containing directory, plus the ".csv" file extension.  For example, in the directory ```terms-versions```, the file ```terms-versions.csv``` is the primary metadata file.  The file with name ending in "-column-mappings.csv" (example: ```terms-versions-column-mappings.csv```) maps the columns of the primary version metadata file to standard properties.  The file with name ending in "-replacements.csv" (example: ```terms-versions-replacements.csv```) is a link table that links versions to versions that replace them.  Other files in the directory contain configuration or other information needed to generate machine readable metadata for the versions described in the directory.  

## 4 Relationships of directories to resources in the TDWG Standards model

 | Level | Current resource IRI pattern | Directory | Version IRI pattern | Directory |
 |---|---|---|---|---|
 | Standard | http://www.tdwg.org/standards/nnn | standards | http://www.tdwg.org/standards/nnn/version/yyyy-mm-dd | standards-versions |
 | Vocabulary | http://rs.tdwg.org/vvv/ | vocabularies | http://rs.tdwg.org/version/vvv/yyyy-mm-dd | vocabularies-versions|
 | Term List | http://rs.tdwg.org/vvv/sss/ | term-lists | http://rs.tdwg.org/vvv/version/sss/yyyy-mm-dd | term-lists-versions |
 | Terms defined by Audubon Core | http://rs.tdwg.org/ac/terms/ttt | audubon | http://rs.tdwg.org/ac/terms/version/ttt-yyyy-mm-dd |
 | Terms borrowed by Audubon Core* | various IRI forms | ac-borrowed | (version metadata not yet recorded) | N/A |
 | Basic Darwin Core terms | http://rs.tdwg.org/dwc/terms/ttt | terms | http://rs.tdwg.org/dwc/terms/version/ttt-yyyy-mm-dd | terms-versions |
 | Darwin Core IRI-value terms | http://rs.tdwg.org/dwc/iri/ttt | iri | http://rs.tdwg.org/dwc/iri/version/ttt-yyyy-mm-dd | iri-versions |
 | dc: terms borrowed by Darwin Core | http://purl.org/dc/elements/1.1/ttt | dc-for-dwc | http://dublincore.org/usage/terms/history/#ttt-nnn | dc-for-dwc-versions |
 | dcterms: terms borrowed by Darwin Core | http://purl.org/dc/terms/ttt | dcterms-for-dwc | http://dublincore.org/usage/terms/history/#ttt-nnn | dcterms-for-dwc-versions |
 |---|---|---|---|---|
 | TDWG utility terms (not part of a standard) | http://rs.tdwg.org/dwc/terms/attributes/ttt | utility | http://rs.tdwg.org/dwc/terms/attributes/version/ttt-yyyy-mm-dd | utility-versions |
 |---|---|---|---|---|
 |obsolete DwC type terms | http://rs.tdwg.org/dwc/dwctype/ttt | dwctype | http://rs.tdwg.org/dwc/dwctype/version/ttt-yyyy-mm-dd |dwctype-versions |
 |obsolete DwC curatorial terms | http://rs.tdwg.org/dwc/curatorial/ttt | curatorial | http://rs.tdwg.org/dwc/curatorial/version/ttt-yyyy-mm-dd |curatorial-versions |
 |obsolete DwC dwcore terms | http://rs.tdwg.org/dwc/dwcore/ttt | dwcore | http://rs.tdwg.org/dwc/dwcore/version/ttt-yyyy-mm-dd |dwcore-versions |
 |obsolete DwC geospatial terms | http://rs.tdwg.org/dwc/geospatial/ttt | geospatial | http://rs.tdwg.org/dwc/geospatial/version/ttt-yyyy-mm-dd |geospatial-versions |
 |obsolete DwC non-TDWG terms | various IRI forms | dwc-obsolete | various IRI forms |dwc-obsolete-versions |



 \* This list will eventually be replaced by a list for each namespace.
