---
permalink: /pw/
---

# Pathway Controlled Vocabulary

**Title:**  Darwin Core Chronometric Age Extension Vocabulary

**Namespace URI:** http://rs.tdwg.org/chrono/terms/

**Preferred namespace abbreviation:** chrono:

**Date version issued:** put ratification date here

**Date created:** put ratification date here

**Part of TDWG Standard:** http://www.tdwg.org/standards/x

**This version:** http://rs.tdwg.org/chrono/doc/list/iso-date-here

**Latest version:** http://rs.tdwg.org/chrono/doc/list/

**Abstract:** someting here

**Contributors:** John Wieczorek, Laura Brenskelle, Robert Guralnick, Kitty Emery, Michelle LeFebvre, Denné Reed

**Creator:** TDWG Darwin Core Chronometric Age Extension Task Group

**Bibliographic citation:** TDWG Darwin Core Chronometric Age Extension Task Group. 2020. Darwin Core Chronometric Age Extension Vocabulary. Biodiversity Information Standards (TDWG). <http://rs.tdwg.org/chrono/doc/list/iso-date-here>


## 1 Introduction

something here

### 1.1 Status of the content of this document

In Section 4, the values of the `Term IRI`, and `Definition` are normative. The values of `Term Name` are non-normative, although one can expect that the namespace abbreviation prefix is one commonly used for the term namespace.  `Label` and the values of all other properties (such as `Notes` and `Examples`) are non-normative.

### 1.2 RFC 2119 key words
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## 2 Use of Terms

something here

## 3 Term index


[Chronometric Age](#chrono_ChronometricAge) |
[Chronometric Age Conversion Protocol](#chrono_chronometricAgeConversionProtocol) |
[Chronometric Age ID](#chrono_chronometricAgeID) |
[Chronometric Age Protocol](#chrono_chronometricAgeProtocol) |
[Chronometric Age References](#chrono_chronometricAgeReferences) |
[Chronometric Age Remarks](#chrono_chronometricAgeRemarks) |
[Chronometric Age Uncertainty In Years](#chrono_chronometricAgeUncertaintyInYears) |
[Chronometric Age Uncertainty Method](#chrono_chronometricAgeUncertaintyMethod) |
[Material Dated](#chrono_materialDated) |
[Material Dated ID](#chrono_materialDatedID) |
[Maximum Chronometric Age](#chrono_maximumChronometricAge) |
[Maximum Chronometric Age Reference System](#chrono_maximumChronometricAgeReferenceSystem) |
[Minimum Chronometric Age](#chrono_minimumChronometricAge) |
[Minimum Chronometric Age Reference System](#chrono_minimumChronometricAgeReferenceSystem) |
[Uncalibrated Chronometric Age](#chrono_uncalibratedChronometricAge) |
[Verbatim Chronometric Age](#chrono_verbatimChronometricAge) 

## 4 Vocabulary
<table>
	<thead>
		<tr>
			<th colspan="2"><a id="chrono_ChronometricAge"></a>Term Name  chrono:ChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/ChronometricAge">http://rs.tdwg.org/chrono/terms/ChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/ChronometricAge-2020-08-14">http://rs.tdwg.org/chrono/terms/version/ChronometricAge-2020-08-14</a></td>
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
			<th colspan="2"><a id="chrono_chronometricAgeConversionProtocol"></a>Term Name  chrono:chronometricAgeConversionProtocol</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/chronometricAgeConversionProtocol">http://rs.tdwg.org/chrono/terms/chronometricAgeConversionProtocol</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/chronometricAgeConversionProtocol-2020-08-14">http://rs.tdwg.org/chrono/terms/version/chronometricAgeConversionProtocol-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age Conversion Protocol</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The method used for converting the uncalibratedChronometricAge into a chronometric age in years, as captured in the maximumChronometricAge, maximumChronometricAgeReferenceSystem, minimumChronometricAge, and minimumChronometricAgeReferenceSystem fields.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>For example, calibration of conventional radiocarbon age or the currently accepted age range of a cultural or geological period.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`INTCAL13`, `sequential 6 phase Bayesian model and IntCal13 calibration`</td>
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
			<th colspan="2"><a id="chrono_chronometricAgeID"></a>Term Name  chrono:chronometricAgeID</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/chronometricAgeID">http://rs.tdwg.org/chrono/terms/chronometricAgeID</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/chronometricAgeID-2020-08-14">http://rs.tdwg.org/chrono/terms/version/chronometricAgeID-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age ID</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An identifier for the set of information associated with a ChronometricAge.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>May be a global unique identifier or an identifier specific to the dataset. This can be used to link this record to another repository where more information about the dataset is shared.</td>
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
			<th colspan="2"><a id="chrono_chronometricAgeProtocol"></a>Term Name  chrono:chronometricAgeProtocol</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/chronometricAgeProtocol">http://rs.tdwg.org/chrono/terms/chronometricAgeProtocol</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/chronometricAgeProtocol-2020-08-14">http://rs.tdwg.org/chrono/terms/version/chronometricAgeProtocol-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age Protocol</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A description of or reference to the methods used to determine the chronometric age.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`radiocarbon AMS`, `K-Ar dates for the lower most marker tuff`, `historic documentation`, `ceramic seriation`</td>
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
			<th colspan="2"><a id="chrono_chronometricAgeReferences"></a>Term Name  chrono:chronometricAgeReferences</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/chronometricAgeReferences">http://rs.tdwg.org/chrono/terms/chronometricAgeReferences</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/chronometricAgeReferences-2020-08-14">http://rs.tdwg.org/chrono/terms/version/chronometricAgeReferences-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age References</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A list (concatenated and separated) of identifiers (publication, bibliographic reference, global unique identifier, URI) of literature associated with the ChronometricAge.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>Recommended best practice is to separate the values in a list with space vertical bar space ( | ).</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`Pluckhahn, Thomas J., Neill J. Wallis, and Victor D. Thompson. 2020  The History and Future of Migrationist Explanation in the Archaeology of the Eastern Woodlands: A Review and Case Study of the Woodland Period Gulf Coast. Journal of Archaeological Research. <a href="https://doi.org/10.1007/s10814-019-09140-x`">https://doi.org/10.1007/s10814-019-09140-x`</a></td>
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
			<th colspan="2"><a id="chrono_chronometricAgeRemarks"></a>Term Name  chrono:chronometricAgeRemarks</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/chronometricAgeRemarks">http://rs.tdwg.org/chrono/terms/chronometricAgeRemarks</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/chronometricAgeRemarks-2020-08-14">http://rs.tdwg.org/chrono/terms/version/chronometricAgeRemarks-2020-08-14</a></td>
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
			<td>`Beta Analytic number: 323913 | One of the Crassostrea virginica right valve specimens from North Midden Feature 17 was chosen for AMS dating, but it is unclear exactly which specimen it was.`</td>
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
			<th colspan="2"><a id="chrono_chronometricAgeUncertaintyInYears"></a>Term Name  chrono:chronometricAgeUncertaintyInYears</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/chronometricAgeUncertaintyInYears">http://rs.tdwg.org/chrono/terms/chronometricAgeUncertaintyInYears</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/chronometricAgeUncertaintyInYears-2020-08-14">http://rs.tdwg.org/chrono/terms/version/chronometricAgeUncertaintyInYears-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age Uncertainty In Years</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The temporal uncertainty of the maximumChronometricAge and minimumChronometicAge in years.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>This is the +/- number for the age in years. The expected unit for this field is years.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`100`</td>
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
			<th colspan="2"><a id="chrono_chronometricAgeUncertaintyMethod"></a>Term Name  chrono:chronometricAgeUncertaintyMethod</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/chronometricAgeUncertaintyMethod">http://rs.tdwg.org/chrono/terms/chronometricAgeUncertaintyMethod</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/chronometricAgeUncertaintyMethod-2020-08-14">http://rs.tdwg.org/chrono/terms/version/chronometricAgeUncertaintyMethod-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Chronometric Age Uncertainty Method</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The method used to generate the value of chronometricAgeUncertaintyInYears.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`2-sigma calibrated range`, `Half of 95% confidence interval`</td>
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
			<th colspan="2"><a id="chrono_materialDated"></a>Term Name  chrono:materialDated</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/materialDated">http://rs.tdwg.org/chrono/terms/materialDated</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/materialDated-2020-08-14">http://rs.tdwg.org/chrono/terms/version/materialDated-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Material Dated</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>A description of the material on which the chronometricAgeProtocol was actually performed, if known.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`Double Tuff`, `Charcoal found in Stratum V`, `charred wood`, `tooth`</td>
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
			<th colspan="2"><a id="chrono_materialDatedID"></a>Term Name  chrono:materialDatedID</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/materialDatedID">http://rs.tdwg.org/chrono/terms/materialDatedID</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/materialDatedID-2020-08-14">http://rs.tdwg.org/chrono/terms/version/materialDatedID-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Material Dated ID</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>An identifier for the material on which the chronometricAgeProtocol was performed, if applicable.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`dwc:occurrenceID: 702b306d-f167-44d0-a5c9-890ece2b8839`, `<a href="https://www.idigbio.org/portal/records/e1438058-c8b9-418e-998e-1e497a3bcec4`">https://www.idigbio.org/portal/records/e1438058-c8b9-418e-998e-1e497a3bcec4`</a></td>
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
			<th colspan="2"><a id="chrono_maximumChronometricAge"></a>Term Name  chrono:maximumChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/maximumChronometricAge">http://rs.tdwg.org/chrono/terms/maximumChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/maximumChronometricAge-2020-08-14">http://rs.tdwg.org/chrono/terms/version/maximumChronometricAge-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Maximum Chronometric Age</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Upper limit for the age of a specimen as determined by a dating method.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The expected unit for this field is years. This field, if populated, must have an associated maximumChronometricAgeReferenceSystem.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`27`</td>
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
			<th colspan="2"><a id="chrono_maximumChronometricAgeReferenceSystem"></a>Term Name  chrono:maximumChronometricAgeReferenceSystem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/maximumChronometricAgeReferenceSystem">http://rs.tdwg.org/chrono/terms/maximumChronometricAgeReferenceSystem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/maximumChronometricAgeReferenceSystem-2020-08-14">http://rs.tdwg.org/chrono/terms/version/maximumChronometricAgeReferenceSystem-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Maximum Chronometric Age Reference System</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The reference system associated with the maximumChronometricAge.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`kya`,`mya`,`BP`,`AD`,`BCE`</td>
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
			<th colspan="2"><a id="chrono_minimumChronometricAge"></a>Term Name  chrono:minimumChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/minimumChronometricAge">http://rs.tdwg.org/chrono/terms/minimumChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/minimumChronometricAge-2020-08-14">http://rs.tdwg.org/chrono/terms/version/minimumChronometricAge-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Minimum Chronometric Age</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>Lower limit for the age of a specimen as determined by a dating method.</td>
		</tr>
		<tr>
			<td>Notes</td>
			<td>The expected unit for this field is years. This field, if populated, must have an associated maximumChronometricAgeReferenceSystem.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`100`</td>
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
			<th colspan="2"><a id="chrono_minimumChronometricAgeReferenceSystem"></a>Term Name  chrono:minimumChronometricAgeReferenceSystem</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/minimumChronometricAgeReferenceSystem">http://rs.tdwg.org/chrono/terms/minimumChronometricAgeReferenceSystem</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/minimumChronometricAgeReferenceSystem-2020-08-14">http://rs.tdwg.org/chrono/terms/version/minimumChronometricAgeReferenceSystem-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Minimum Chronometric Age Reference System</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The reference system associated with the minimumChronometricAge.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`kya`,`mya`,`BP`,`AD`,`BCE`</td>
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
			<th colspan="2"><a id="chrono_uncalibratedChronometricAge"></a>Term Name  chrono:uncalibratedChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/uncalibratedChronometricAge">http://rs.tdwg.org/chrono/terms/uncalibratedChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/uncalibratedChronometricAge-2020-08-14">http://rs.tdwg.org/chrono/terms/version/uncalibratedChronometricAge-2020-08-14</a></td>
		</tr>
		<tr>
			<td>Label</td>
			<td>Uncalibrated Chronometric Age</td>
		</tr>
		<tr>
			<td>Definition</td>
			<td>The output of a dating assay before it is calibrated into an age using a specific conversion protocol.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`1510 +/- 25 14C yr BP`, `16.26 Ma +/- 0.016`</td>
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
			<th colspan="2"><a id="chrono_verbatimChronometricAge"></a>Term Name  chrono:verbatimChronometricAge</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Term IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/verbatimChronometricAge">http://rs.tdwg.org/chrono/terms/verbatimChronometricAge</a></td>
		</tr>
		<tr>
			<td>Modified</td>
			<td>2020-08-14</td>
		</tr>
		<tr>
			<td>Term version IRI</td>
			<td><a href="http://rs.tdwg.org/chrono/terms/version/verbatimChronometricAge-2020-08-14">http://rs.tdwg.org/chrono/terms/version/verbatimChronometricAge-2020-08-14</a></td>
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
			<td>Notes</td>
			<td>For example, this could be the radiocarbon age as given in an AMS dating report. This could also be simply what is reported as the age of a specimen in legacy collections data.</td>
		</tr>
		<tr>
			<td>Examples</td>
			<td>`27 BC to 14 AD`, `stratigraphically pre-1104`</td>
		</tr>
		<tr>
			<td>Type</td>
			<td>Property</td>
		</tr>
	</tbody>
</table>


