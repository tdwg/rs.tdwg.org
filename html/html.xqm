xquery version "3.1";

module namespace html = 'http://rs.tdwg.com/html';

declare function html:subdomain()
{
  normalize-space(http:send-request(<http:request method='get' href='https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/html/subdomain.txt'/>)[2])
};

declare function html:branch()
{
  normalize-space(http:send-request(<http:request method='get' href='https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/html/branch.txt'/>)[2])
};

declare function html:load-term-list-lookup() as element()*
{
(: The term list table has columns containing the term list database name, abbreviations, etc. :)
let $lookupDoc := http:send-request(<http:request method='get' href='{"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/term-lists/term-lists.csv"}'/>)[2]
let $xmlLookup := csv:parse($lookupDoc, map { 'header' : true(),'separator' : "," })
return $xmlLookup/csv
};

(: Looks up the name of the database that contains the metadata for the terms in a term list :)
declare function html:find-list-dbname($list_localName as xs:string) as xs:string
{
(: Note: there should be one database name for one list URI, so only a single string should ever get returned :)
let $lists := html:load-term-list-lookup()
for $list in $lists/record
where $list/list/text() = $list_localName
return $list/database/text()
};

(: Looks up the name of the database that contains the metadata for the terms in a term version list :)
declare function html:find-list-version-dbname($list_localName as xs:string) as xs:string
{
(: Note: there should be one database version name for one list URI, so only a single string should ever get returned :)
let $lists := html:load-term-list-lookup()
for $list in $lists/record
where $list/list/text() = $list_localName
return $list/versions_database/text()
};

(: Looks up the abbreviation for the namespace associated with terms in a term list :)
declare function html:find-list-ns-abbreviation($list_localName as xs:string) as xs:string
{
(: Note: there should be one database namespace abbreviation for each list URI, so only a single string should ever get returned :)
let $lists := html:load-term-list-lookup()
for $list in $lists/record
where $list/list/text() = $list_localName
return $list/vann_preferredNamespacePrefix/text()
};

(: Looks up the standard that a term list is associated with :)
declare function html:find-standard-for-list($list_uri as xs:string) as xs:string
{
(: Note: there should be one standard for each list URI, so only a single string should ever get returned :)
let $lists := html:load-term-list-lookup()
let $result := 
  for $list in $lists/record
  where $list/list/text() = $list_uri
  return $list/standard/text()
return
      (: If the term list is not part of any standard, or matches with two standards, return an empty string :)
      if (count($result)=1)
      then  $result
      else  ""
};

(: Looks up the term list version namespace that corresponds to a term list :)
declare function html:find-version-for-list($list_localName as xs:string) as xs:string
{
(: Note: there should be one version URI for each list URI, so only a single string should ever get returned :)
let $lists := html:load-term-list-lookup()
let $result := 
  for $list in $lists/record
  where $list/list/text() = $list_localName
  return $list/versions_uri/text()
return
      (: If the term list doesn't have versions (like decisions), or matches with two version files, return an empty string :)
      if (count($result)=1)
      then  $result
      else  ""
};

(:--------------------------------------------------------------------------------------------------:)
(: utility functions :)

(: from http://www.xqueryfunctions.com/xq/ :)
declare function html:substring-before-last
  ( $arg as xs:string? ,
    $delim as xs:string )  as xs:string {

   if (matches($arg, html:escape-for-regex($delim)))
   then replace($arg,
            concat('^(.*)', html:escape-for-regex($delim),'.*'),
            '$1')
   else ''
 } ;
 
 (: from http://www.xqueryfunctions.com/xq/ :)
 declare function html:escape-for-regex
  ( $arg as xs:string? )  as xs:string {

   replace($arg,
           '(\.|\[|\]|\\|\||\-|\^|\$|\?|\*|\+|\{|\}|\(|\))','\\$1')
 } ;

declare function html:load-configuration($repoPath as xs:string,$repoName as xs:string) as node()*
{
let $constantsDoc := http:send-request(<http:request method='get' href='{$repoPath||$repoName||'/constants.csv'}'/>)[2]
let $xmlConstants := csv:parse($constantsDoc, map { 'header' : true(),'separator' : "," })
return $xmlConstants/csv/record
};

(: go through the term list or list versions records and pull the metadata for the particular list. There should be exactly one record element returned :)
declare function html:load-metadata-record($list-iri as xs:string,$db as xs:string) as node()*
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)
let $key := $config/baseIriColumn/text() (: determine which column in the source table contains the primary key for the record :)
let $coreDoc := $config/coreClassFile/text()
let $metadataSeparator := $config/separator/text()
let $metadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

for $record in $metadata
where $record/*[local-name()=$key]/text()=$list-iri (: the primary key of the record row must match the requested list :)
return $record
};

(: Load the metadata for the classes that are linked to the core class :)
declare function html:generateLinkedMetadata($db as xs:string) as node()*
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)
let $metadataSeparator := $config/separator/text()

let $linkedClassesDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||'linked-classes.csv'}'/>)[2]
let $xmlLinkedClasses := csv:parse($linkedClassesDoc, map { 'header' : true(),'separator' : "," })
let $linkedClasses := $xmlLinkedClasses/csv/record

let $linkedMetadata :=
      for $class in $linkedClasses
      let $linkedDoc := $class/filename/text()
      let $linkedClassPrefix := substring-before($linkedDoc,".")

      let $classMappingDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$linkedClassPrefix||"-column-mappings.csv"}'/>)[2]
      let $xmlClassMapping := csv:parse($classMappingDoc, map { 'header' : true(),'separator' : "," })
      let $classClassesDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$linkedClassPrefix||"-classes.csv"}'/>)[2]
      let $xmlClassClasses := csv:parse($classClassesDoc, map { 'header' : true(),'separator' : "," })
      let $classMetadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$linkedDoc}'/>)[2]
      let $xmlClassMetadata := csv:parse($classMetadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
      return
        ( 
        <file>{
          $class/link_column,
          $class/link_property,
          $class/suffix1,
          $class/link_characters,
          $class/suffix2,
          $class/forward_link,
          $class/class,
          <classes>{
            $xmlClassClasses/csv/record
          }</classes>,
          <mapping>{
            $xmlClassMapping/csv/record
          }</mapping>,
          <metadata>{
            $xmlClassMetadata/csv/record
          }</metadata>
       }</file>
       )
return $linkedMetadata

};

(: Generate a sequence of the members of a particular term list version :)
declare function html:generate-list-version-members($termListVersion as xs:string) as xs:string+
{
  let $linkedMetadata := html:generateLinkedMetadata("term-lists-versions")
  let $listsMembers := $linkedMetadata/metadata/record
  for $member in $listsMembers
  where $member/termListVersion/text() = $termListVersion
  order by $member/termVersion/text()
  return $member/termVersion/text()
};

(: Find the standard of which a vocabulary is part :)
declare function html:find-standard($vocabulary as xs:string) as xs:string
{
  let $linkedMetadata := html:generateLinkedMetadata("standards")
  let $parts := $linkedMetadata/metadata/record
  for $part in $parts
  where $part/part/text() = $vocabulary
  return $part/standard/text()
};

(: Generate a sequence of the term lists that are part of a particular vocabulary :)
declare function html:generate-vocabulary-term-list-members($vocabulary as xs:string,$db as xs:string) as xs:string+
{
  let $linkedMetadata := html:generateLinkedMetadata($db)
  let $termLists := $linkedMetadata/metadata/record
  for $termList in $termLists
  where $termList/vocabulary/text() = $vocabulary
  order by $termList/termList/text()
  return $termList/termList/text()
};

(: go through the term list or term list versions records ($db) and pull the metadata for all lists that are part of a particular vocabulary. :)
declare function html:load-list-records($termLists as xs:string+,$db as xs:string) as element()*
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)

let $key := $config/baseIriColumn/text() (: determine which column in the source table contains the primary key for the record :)
let $coreDoc := $config/coreClassFile/text()
let $metadataSeparator := $config/separator/text()
let $metadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

for $record in $metadata,$termList in $termLists
where $record/*[local-name()=$key]/text()=$termList (: the primary key of the record row must match a list in the vocabulary :)

return $record
};

(: generate a table with metadata about a single term :)
declare function html:term-metadata($record as element(),$version as xs:string,$replacements as element()*,$ns as xs:string) as element()
{
   <table>{
   <tr><td><strong>Term Name:</strong></td><td>{$ns||":"||$record/term_localName/text()}</td></tr>,
   <tr><td><strong>Label:</strong></td><td>{$record/label/text()}</td></tr>,
   <tr><td><strong>Term IRI:</strong></td><td>{$record/term_isDefinedBy/text()||$record/term_localName/text()}</td></tr>,
  
   (: terms not defined by TDWG may have different version patterns, or may not have versions :)
   if (contains($record/term_isDefinedBy/text(), html:subdomain() ))
   then (
   <tr><td><strong>Term version IRI:</strong></td><td><a href='{$version}'>{$version}</a></td></tr>
   )
   else (),
  
   <tr><td><strong>Modified:</strong></td><td>{$record/term_modified/text()}</td></tr>,
   <tr><td><strong>Definition:</strong></td><td>{$record/rdfs_comment/text()}</td></tr>,
   
   if (contains($record/rdf_type/text(),"#"))
   then <tr><td><strong>Type:</strong></td><td>{substring-after($record/rdf_type/text(),"#")}</td></tr>
   else <tr><td><strong>Type:</strong></td><td>{$record/rdf_type/text()}</td></tr>,
   
   if ($record/term_deprecated/text() != "")
   then (
   <tr><td><strong>Note:</strong></td><td>This term is no longer recommended for use.</td></tr>
   )
   else (),
   
   if ($record/replaces_term/text() != "")
   then (
     <tr><td><strong>Replaces:</strong></td><td><a href='{$record/replaces_term/text()}'>{$record/replaces_term/text()}</a></td></tr>
     )
   else (),
   if ($record/replaces1_term/text() != "")
   then (
     <tr><td><strong>Replaces:</strong></td><td><a href='{$record/replaces1_term/text()}'>{$record/replaces1_term/text()}</a></td></tr>
     )
   else (),
   if ($record/replaces2_term/text() != "")
   then (
     <tr><td><strong>Replaces:</strong></td><td><a href='{$record/replaces2_term/text()}'>{$record/replaces2_term/text()}</a></td></tr>
     )
   else (),
  
   for $replacement in $replacements
   where $replacement/replaced_term_localName/text() = $record/term_localName/text()
   return <tr><td><strong>Is replaced by:</strong></td><td><a href='{$replacement/replacing_term/text()}'>{$replacement/replacing_term/text()}</a></td></tr>
  
   }</table>
};

(: generate a table with metadata about a single term version :)
declare function html:term-version-metadata($record as element(),$versionOf as xs:string,$replacements as element()*,$ns as xs:string) as element()
{
 <table>{
   <tr><td><a name="{$ns||"_"||$record/term_localName/text()}"><strong>Term Name:</strong></a></td><td>{$ns||":"||$record/term_localName/text()}</td></tr>,
   <tr><td><strong>Label:</strong></td><td>{$record/label/text()}</td></tr>,
   <tr><td><strong>Term version IRI:</strong></td><td>{$record/version/text()}</td></tr>,
   <tr><td><strong>Version of:</strong></td><td><a href='{$versionOf}'>{$versionOf}</a></td></tr>,
   <tr><td><strong>Issued:</strong></td><td>{$record/version_issued/text()}</td></tr>,
   <tr><td><strong>Definition:</strong></td><td>{$record/rdfs_comment/text()}</td></tr>,
   <tr><td><strong>Type:</strong></td><td>{substring-after($record/rdf_type/text(),"#")}</td></tr>,
   <tr><td><strong>Status:</strong></td><td>{$record/version_status/text()}</td></tr>,

   if ($record/replaces_version/text() != "")
   then (
     <tr><td><strong>Replaces:</strong></td><td><a href='{$record/replaces_version/text()}'>{$record/replaces_version/text()}</a></td></tr>
     )
   else (),
   if ($record/replaces1_version/text() != "")
   then (
     <tr><td><strong>Replaces:</strong></td><td><a href='{$record/replaces1_version/text()}'>{$record/replaces1_version/text()}</a></td></tr>
     )
   else (),
   if ($record/replaces2_version/text() != "")
   then (
     <tr><td><strong>Replaces:</strong></td><td><a href='{$record/replaces2_version/text()}'>{$record/replaces2_version/text()}</a></td></tr>
     )
   else (),

   for $replacement in $replacements
   where $replacement/replaced_version_localName/text() = $record/versionLocalName/text()
   return <tr><td><strong>Is replaced by:</strong></td><td><a href='{$replacement/replacing_version/text()}'>{$replacement/replacing_version/text()}</a></td></tr>

   }</table>
};

(: Find the most recent version of a term :)
declare function html:most-recent-version($linkedMetadata as node()+,$localName as xs:string) as xs:string+
{
let $result := 
    for $record in $linkedMetadata
    where $record/term_localName/text() = $localName
    order by $record/version/text()
    return $record/version/text()
return
      (: If there are no versions, return an empty string :)
      if (count($result)=0)
      then  ""
      else  $result

};

(:--------------------------------------------------------------------------------------------------:)
(: Generate term web page //////////////////////////////////////////////////////////////////////////:)
(:--------------------------------------------------------------------------------------------------:)

(: Generate the HTML tables of metadata about the terms in the list and returns them as a div element :)
declare function html:generate-term-html($db as xs:string,$ns as xs:string,$localName as xs:string) as element()
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)

let $coreDoc := $config/coreClassFile/text()
let $metadataSeparator := $config/separator/text()
let $baseIriColumn := $config/baseIriColumn/text()
let $metadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record
let $linkedMetadataRaw := html:generateLinkedMetadata($db)
let $linkedMetadata := $linkedMetadataRaw/metadata/record
return
for $record in $metadata
where $record/*[local-name()=$baseIriColumn]/text()=$localName
let $version := 
  if ($db!="decisions")
  then html:most-recent-version($linkedMetadata,$localName)[last()]
  else ""
return
<html>
  <head>
    <meta charset="utf-8"/>
    <title>{"Term metadata for "||$ns||":"||$localName}</title>
  </head>
  <body>{
    html:term-metadata($record,$version,$linkedMetadata,$ns),
    <br/>,
    <p><strong>Metadata about this term are available in the following formats/serializations:</strong></p>,
    <table border="1">{
      let $iri := $record/term_isDefinedBy/text()||$localName
      return (
      <tr><th>Description</th><th>IRI</th></tr>,
      <tr><td>HTML file (this document)</td><td><a href="{$iri||'.htm'}">{$iri||".htm"}</a></td></tr>,
      <tr><td>RDF/Turtle</td><td><a href="{$iri||'.ttl'}">{$iri||".ttl"}</a></td></tr>,
      <tr><td>RDF/XML</td><td><a href="{$iri||'.rdf'}">{$iri||".rdf"}</a></td></tr>,
      <tr><td>JSON-LD</td><td><a href="{$iri||'.json'}">{$iri||".json"}</a></td></tr>
      )
    }</table>,

    <p>For complete information about the set of terms that includes this one, see <a href="{$record/term_isDefinedBy/text()}">{$record/term_isDefinedBy/text()}</a></p>,
    html:generate-footer()
    }</body>
</html>
};

(:--------------------------------------------------------------------------------------------------:)
(: Generate term version web page //////////////////////////////////////////////////////////////////:)
(:--------------------------------------------------------------------------------------------------:)

(: Generate the HTML tables of metadata about the terms in the list and returns them as a div element :)
declare function html:generate-term-version-html($db as xs:string,$ns as xs:string,$localName as xs:string) as element()
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)

let $coreDoc := $config/coreClassFile/text()
let $metadataSeparator := $config/separator/text()
let $metadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

let $linkedMetadataRaw := html:generateLinkedMetadata($db)
let $replacements := $linkedMetadataRaw/metadata/record

let $listVersionMembersRaw := html:generateLinkedMetadata("term-lists-versions")
let $listVersionMembers := $listVersionMembersRaw/metadata/record

for $record in $metadata
let $versionRoot := substring($record/version/text(),1,
fn:string-length($record/version/text())-11) (: find the part of the version before the ISO 8601 date :)
let $versionOf := replace($versionRoot,'version/','')
where $record/versionLocalName/text() = $localName
return 
<html>
  <head>
    <meta charset="utf-8"/>
    <title>{"Metadata for the "||$record/version_issued/text()||" version of the term "||$ns||":"||$record/term_localName/text()}</title>
  </head>
  <body>{
     <strong>{"Metadata for the "||$record/version_issued/text()||" version of the term "||$ns||":"||$record/term_localName/text()}</strong>,
     <br/>,
    html:term-version-metadata($record,$versionOf,$replacements,$ns),
    <br/>,
    <p><strong>Metadata about this term version are available in the following formats/serializations:</strong></p>,
    <table border="1">{
      let $iri := $record/version/text()
      return (
      <tr><th>Description</th><th>IRI</th></tr>,
      <tr><td>HTML file (this document)</td><td><a href="{$iri||'.htm'}">{$iri||".htm"}</a></td></tr>,
      <tr><td>RDF/Turtle</td><td><a href="{$iri||'.ttl'}">{$iri||".ttl"}</a></td></tr>,
      <tr><td>RDF/XML</td><td><a href="{$iri||'.rdf'}">{$iri||".rdf"}</a></td></tr>,
      <tr><td>JSON-LD</td><td><a href="{$iri||'.json'}">{$iri||".json"}</a></td></tr>
      )
    }</table>,
    <p><span>For more information about this term version in the context of sets of terms that include it, please refer to the following term list versions: </span><br/>
    {
    for $listVersion in $listVersionMembers
    where $listVersion/termVersion/text() = $record/version/text()
    return (<a href="{$listVersion/termListVersion/text()}">{$listVersion/termListVersion/text()}</a>,<br/>)
    }</p>,
    html:generate-footer()
    }</body>
</html>
};

(:--------------------------------------------------------------------------------------------------:)
(: Generate vocabulary web page ////////////////////////////////////////////////////////////////////:)
(:--------------------------------------------------------------------------------------------------:)

(: 1st level function :)

(: Generates web page for a vocabulary; usually following the pattern http://rs.tdwg.org/{vocab}/ :)
declare function html:generate-vocabulary-html($vocabularyIri as xs:string) as element()
{
let $vocabularyMetadata := html:load-metadata-record($vocabularyIri,"vocabularies")

return
<html>
  <head>
    <meta charset="utf-8"/>
    <title>{$vocabularyMetadata/label/text()}</title>
  </head>
  <body>{
    html:generate-vocabulary-metadata-html($vocabularyMetadata),
    html:generate-vocabulary-toc-etc-html($vocabularyIri),
    html:generate-vocabulary-table-html($vocabularyIri),
    html:generate-footer()
   }</body>
</html>
};

(:--------------------------------------------------------------------------------------------------:)
(: 2nd level functions :)

(: Generates HTML metadata for a particular vocabulary and returns them as a div element :)
declare function html:generate-vocabulary-metadata-html($record as element()) as element()
{
let $thisVersion := html:subdomain()||"version/"||$record/vocabulary_localName/text()||$record/vocabulary_modified/text()
let $std := html:find-standard($record/vocabulary/text())
return  
<div>{
  <strong>Title: </strong>,<span>{$record/label/text()}</span>,<br/>,
  <strong>Date version issued: </strong>,<span>{$record/vocabulary_modified/text()}</span>,<br/>,
  <strong>Date created: </strong>,<span>{$record/vocabulary_created/text()}</span>,<br/>,

  if ($std != "")
  then (
    <strong>Part of TDWG Standard: </strong>,<a href='{$std}'>{$std}</a>,<br/>
    )
  else (
    <span>Not part of any TDWG Standard</span>,<br/>
    ),
  
  <strong>This version: </strong>,<a href='{$thisVersion}'>{$thisVersion}</a>,<br/>,
  <strong>Latest version: </strong>,<a href='{$record/vocabulary/text()}'>{$record/vocabulary/text()}</a>,<br/>,
  <strong>Abstract: </strong>,<span>{$record/description/text()}</span>,<br/>,
  <strong>Creator: </strong>,<span>{$record/dc_creator/text()}</span>,<br/>,
  
  if ($record/vocabulary_deprecated/text() = "true")
  then (
    <strong>Status note: </strong>,<span>This vocabulary has been deprecated and is no longer recommended for use.</span>,<br/>
    )
  else (),
  <br/>
  
}</div>
};

(: Generates the HTML for the middle section of the vocabulary page and returns it as a div elelment :)
declare function html:generate-vocabulary-toc-etc-html($vocabularyIri as xs:string) as element()
{
<div>
  <h1>Table of Contents</h1>
  <ul style="list-style: none;">
    <li><a href="#1">1 Introduction</a></li>
    <li><a href="#2">2 Vocabulary versions</a></li>
    <li><a href="#3">3 Vocabulary distributions</a></li>
    <li><a href="#4">4 Term lists that are part of this vocabulary</a></li>
  </ul>
  <h1><a id="1">1 Introduction</a></h1>
  <p>This document provides access to the parts and history of this vocabulary.  A TDWG vocabulary is composed of term lists that have been minted by TDWG as part of this vocabulary, or that may be composed of terms borrowed from other vocabularies within or outisde of TDWG.  The vocabulary changes over time as those lists change, or as new term lists are added to the vocabulary.  These changes are documented by versions of the vocabulary, which are &quot;snapshots&quot; of the vocabulary at the time that the version was issued.</p>
  <p>For more information about the structure and version model of TDWG vocabularies, see the <a href="http://www.tdwg.org/standards/147">TDWG Standards Documentation Specification</a>.</p>
  <h1><a id="2">2 Vocabulary versions</a></h1>
  <p>To examine specific historical versions of this vocabulary, click on one of the links below.</p>
  <ul style="list-style: none;">{

    let $linkedMetadata := html:generateLinkedMetadata("vocabularies")
    let $versions := $linkedMetadata/metadata/record
    for $version in $versions
    where $version/vocabulary/text() = $vocabularyIri and exists($version/version) (: screen out other linked metadata not related to versions:)
    return <li><a href="{$version/version/text()}">{$version/version/text()}</a></li>
  }</ul>
  <h1><a id="3">3 Vocabulary distributions</a></h1>
  <p>This vocabulary is available in the formats or distribution methods listed in the table below.  Please note that distribution access URLs may be subject to change over time.  Therefore, it is preferable to request the abstract IRI of the resources and request the desired Content-type through content negotiation.</p>
  <table border="1">{
    let $iri := html:substring-before-last($vocabularyIri,"/")
    return (
    <tr><th>Description</th><th>IRI</th><th>Access URL</th></tr>,
    <tr><td>HTML file (this document)</td><td>{$iri||".htm"}</td><td><a href="{$iri||'.htm'}">{$iri||".htm"}</a></td></tr>,
    <tr><td>RDF/Turtle</td><td>{$iri||".ttl"}</td><td><a href="{$iri||'.ttl'}">{$iri||".ttl"}</a></td></tr>,
    <tr><td>RDF/XML</td><td>{$iri||".rdf"}</td><td><a href="{$iri||'.rdf'}">{$iri||".rdf"}</a></td></tr>,
    <tr><td>JSON-LD</td><td>{$iri||".json"}</td><td><a href="{$iri||'.json'}">{$iri||".json"}</a></td></tr>
    )
  }</table>
  <h1><a id="4">4 Term lists that are part of this vocabulary</a></h1>
</div>
};

(: Generate the HTML tables of metadata about the term lists in the vocabulary and returns them as a div element :)
declare function html:generate-vocabulary-table-html($vocabularyIri as xs:string) as element()
{
let $termLists := html:generate-vocabulary-term-list-members($vocabularyIri,"vocabularies") (: generate sequence of term list IRIs that are in vocabulary:)
let $metadata := html:load-list-records($termLists,"term-lists") (: pull the metadata records for term lists in the sequence :)
  
return 
     <div>
       {
       for $record in $metadata
       order by $record/list_localName/text()
       return (
         <table>{
         <tr><td><strong>Label:</strong></td><td>{$record/label/text()}</td></tr>,
         <tr><td><strong>List IRI:</strong></td><td><a href='{$record/list/text()}'>{$record/list/text()}</a></td></tr>,
         <tr><td><strong>Modified:</strong></td><td>{$record/list_modified/text()}</td></tr>,
         <tr><td><strong>Description:</strong></td><td>{$record/description/text()}</td></tr>,
         
         if ($record/list_deprecated/text() != "")
         then (
         <tr><td><strong>Note:</strong></td><td>This list is no longer recommended for use.</td></tr>
         )
         else ()
         }</table>,<br/>
         )
       }
     </div>
};

(: Generate a footer and return it as a div element :)
declare function html:generate-footer() as element()
{
<div>
  <hr/>
  <p>Content on this site, made open by <a href="http://www.tdwg.org/">Biodiversity Information Standards (TDWG)</a> is licensed under a <a href="http://creativecommons.org/licenses/by/4.0/" target="_blank">Creative Commons Attribution 4.0 International License</a>.</p>
</div>
};

(:--------------------------------------------------------------------------------------------------:)
(: Generate vocabulary version web page ////////////////////////////////////////////////////////////:)
(:--------------------------------------------------------------------------------------------------:)

(: 1st level function :)

(: Generates web page for a vocabulary version; usually following the pattern http://rs.tdwg.org/version/{vocab}/{iso-date} :)
declare function html:generate-vocabulary-version-html($vocabularyVersionIri as xs:string) as element()
{
let $vocabularyVersionMetadata := html:load-metadata-record($vocabularyVersionIri,"vocabularies-versions")

return
<html>
  <head>
    <meta charset="utf-8"/>
    <title>{$vocabularyVersionMetadata/label/text()||" "||$vocabularyVersionMetadata/version_issued/text()||" version"}</title>
  </head>
  <body>{
    html:generate-vocabulary-version-metadata-html($vocabularyVersionMetadata),
    html:generate-vocabulary-version-toc-etc-html($vocabularyVersionIri),
    html:generate-vocabulary-version-table-html($vocabularyVersionIri),
    html:generate-footer()
   }</body>
</html>
};

(:--------------------------------------------------------------------------------------------------:)
(: 2nd level functions :)

(: Generates HTML metadata for a particular vocabulary version and returns them as a div element :)
declare function html:generate-vocabulary-version-metadata-html($record as element()) as element()
{
let $std := html:find-standard($record/vocabulary/text())

let $linkedMetadataRaw := html:generateLinkedMetadata("vocabularies-versions")
let $replacements := $linkedMetadataRaw/metadata/record

return  
<div>{
  <strong>Title: </strong>,<span>{$record/label/text()||" (version)"}</span>,<br/>,
  <strong>Issued: </strong>,<span>{$record/version_issued/text()}</span>,<br/>,
  <strong>Part of TDWG Standard: </strong>,<a href='{$std}'>{$std}</a>,<br/>,
  <strong>This version: </strong>,<a href='{$record/version/text()}'>{$record/version/text()}</a>,<br/>,
  <strong>Version status: </strong>,<span>{$record/vocabulary_status/text()}</span>,<br/>,
  <strong>Latest version: </strong>,<a href='{$record/vocabulary/text()}'>{$record/vocabulary/text()}</a>,<br/>,

  for $replacement in $replacements
  where $replacement/replacing_vocabulary/text() = $record/version/text()
  return (<strong>Previous version:</strong>,<a href='{$replacement/replaced_vocabulary/text()}'>{$replacement/replaced_vocabulary/text()}</a>,<br/>),

  for $replacement in $replacements
  where $replacement/replaced_vocabulary/text() = $record/version/text()
  return (<strong>Replaced by:</strong>,<a href='{$replacement/replacing_vocabulary/text()}'>{$replacement/replacing_vocabulary/text()}</a>,<br/>),

  <strong>Abstract: </strong>,<span>{$record/description/text()}</span>,<br/>,
  <strong>Creator: </strong>,<span>{$record/dc_creator/text()}</span>,<br/>,
  <br/>
  
}</div>
};

(: Generates the HTML for the middle section of the term list versions page and returns it as a div elelment :)
declare function html:generate-vocabulary-version-toc-etc-html($vocabularyVersionIri as xs:string) as element()
{
<div>
  <h1>Table of Contents</h1>
  <ul style="list-style: none;">
    <li><a href="#1">1 Introduction</a></li>
    <li><a href="#2">2 Vocabulary version distributions</a></li>
    <li><a href="#3">3 Term list versions that were part of this vocabulary when this version of it was issued</a></li>
  </ul>
  <h1><a id="1">1 Introduction</a></h1>
  <p>A TDWG vocabulary is composed of term lists that have been minted by TDWG as part of that vocabulary, or that may be composed of terms borrowed from other vocabularies within or outisde of TDWG.  The vocabulary changes over time as those lists change, or as new term lists are added to the vocabulary.</p> 
  <p>This vocabulary version is a &quot;snapshot&quot; of the vocabulary at a particular moment in time.  The term list versions listed below includes those that were part of the vocabulary at the time this version was issued.  The status of an individual term list may have changed since the time that the vocabulary version was issued.  The version status indicates the status of the list at the present time, not at the time the vocabulary was issued.</p>
  <p>For more information about the structure and version model of TDWG vocabularies, see the <a href="http://www.tdwg.org/standards/147">TDWG Standards Documentation Specification</a>.</p>
  <h1><a id="2">2 Vocabulary version distributions</a></h1>
  <p>This vocabulary versions list is available in the formats or distribution methods listed in the table below.  Please note that distribution access URLs may be subject to change over time.  Therefore, it is preferable to request the abstract IRI of the resources and request the desired Content-type through content negotiation.</p>
  <table border="1">{
    let $iri := $vocabularyVersionIri
    return (
    <tr><th>Description</th><th>IRI</th><th>Access URL</th></tr>,
    <tr><td>HTML file (this document)</td><td>{$iri||".htm"}</td><td><a href="{$iri||'.htm'}">{$iri||".htm"}</a></td></tr>,
    <tr><td>RDF/Turtle</td><td>{$iri||".ttl"}</td><td><a href="{$iri||'.ttl'}">{$iri||".ttl"}</a></td></tr>,
    <tr><td>RDF/XML</td><td>{$iri||".rdf"}</td><td><a href="{$iri||'.rdf'}">{$iri||".rdf"}</a></td></tr>,
    <tr><td>JSON-LD</td><td>{$iri||".json"}</td><td><a href="{$iri||'.json'}">{$iri||".json"}</a></td></tr>
    )
  }</table>
  <h1><a id="3">3 Term list versions that were part of this vocabulary when this version of it was issued</a></h1>
</div>
};

(: Generate the HTML tables of metadata about the term lists in the vocabulary and returns them as a div element :)
declare function html:generate-vocabulary-version-table-html($vocabularyVersionIri as xs:string) as element()
{
let $termListsVersions := html:generate-vocabulary-term-list-members($vocabularyVersionIri,"vocabularies-versions") (: generate sequence of term list version IRIs that are in vocabulary:)
let $metadata := html:load-list-records($termListsVersions,"term-lists-versions") (: pull the metadata records for term lists versions in the sequence :)

let $linkedMetadataRaw := html:generateLinkedMetadata("term-lists-versions")
let $replacements := $linkedMetadataRaw/metadata/record
  
return 
     <div>
       {
       for $record in $metadata
       order by $record/list_localName/text()
       return (
         <table>{
         <tr><td><strong>Label:</strong></td><td>{$record/label/text()}</td></tr>,
         <tr><td><strong>List version IRI:</strong></td><td><a href='{$record/version/text()}'>{$record/version/text()}</a></td></tr>,
         <tr><td><strong>Modified:</strong></td><td>{$record/version_modified/text()}</td></tr>,
         <tr><td><strong>Description:</strong></td><td>{$record/description/text()}</td></tr>,
         <tr><td><strong>Status:</strong></td><td>{$record/status/text()}</td></tr>,

          for $replacement in $replacements
          where $replacement/replacing_list/text() = $record/version/text()
          return (<tr><td><strong>Previous version:</strong></td><td><a href='{$replacement/replaced_list/text()}'>{$replacement/replaced_list/text()}</a></td></tr>),
        
          for $replacement in $replacements
          where $replacement/replaced_list/text() = $record/version/text()
          return (<tr><td><strong>Replaced by:</strong></td><td><a href='{$replacement/replacing_list/text()}'>{$replacement/replacing_list/text()}</a></td></tr>)

         }</table>,<br/>
         )
       }
     </div>
};

(:--------------------------------------------------------------------------------------------------:)
(: Generate decisions web page ////////////////////////////////////////////////////////////////////:)
(:--------------------------------------------------------------------------------------------------:)

(: 1st level function :)

(: Generates web page for the decisions list; ; following the pattern http://rs.tdwg.org/decisions/ :)
(: Note: at the moment, this is just a hack of the term lists web page.  It shoud be modified to produce the actual decisions page. :)
declare function html:generate-decisions-html($termListIri as xs:string) as element()
{
let $listMetadata := html:load-metadata-record($termListIri,"term-lists")
let $ns := html:find-list-ns-abbreviation($termListIri)
let $std := html:find-standard-for-list($termListIri)
let $version := html:find-version-for-list($termListIri)
return
<html>
  <head>
    <meta charset="utf-8"/>
    <title>{$listMetadata/label/text()}</title>
  </head>
  <body>{
    html:generate-list-metadata-html($listMetadata,$std,$version),
    html:generate-list-toc-etc-html($termListIri),
    html:generate-list-html(html:find-list-dbname($termListIri),$ns),
    html:generate-footer()
   }</body>
</html>
};

(:--------------------------------------------------------------------------------------------------:)
(: Generate term lists web page ////////////////////////////////////////////////////////////////////:)
(:--------------------------------------------------------------------------------------------------:)

(: 1st level function :)

(: Generates web page for a term list; ; usually following the pattern http://rs.tdwg.org/{vocab}/{list}/ :)
declare function html:generate-term-list-html($termListIri as xs:string) as element()
{
let $listMetadata := html:load-metadata-record($termListIri,"term-lists")
let $ns := html:find-list-ns-abbreviation($termListIri)
let $std := html:find-standard-for-list($termListIri)
let $version := html:find-version-for-list($termListIri)
return
<html>
  <head>
    <meta charset="utf-8"/>
    <title>{$listMetadata/label/text()}</title>
  </head>
  <body>{
    html:generate-list-metadata-html($listMetadata,$std,$version),

  if ($termListIri = html:subdomain()||"dwc/terms/")
  then (
    <h1>Note: This is the list of core terms defined by Darwin Core. For the <a href="https://dwc.tdwg.org/terms/">Darwin Core Quick Reference Guide</a>, please bookmark <a href="https://dwc.tdwg.org/terms/">https://dwc.tdwg.org/terms/</a><br/></h1>
    )
  else (),

    html:generate-list-toc-etc-html($termListIri),
    html:generate-list-html(html:find-list-dbname($termListIri),$ns),
    html:generate-footer()
   }</body>
</html>
};

(:--------------------------------------------------------------------------------------------------:)
(: 2nd level functions :)

(: Generates HTML metadata for a particular list and returns them as a div element :)
declare function html:generate-list-metadata-html($record as element(),$std as xs:string,$version as xs:string) as element()
{
let $thisVersion := $version||$record/list_modified/text()
return  
<div>{
  <strong>Title: </strong>,<span>{$record/label/text()}</span>,<br/>,
  <strong>Date version issued: </strong>,<span>{$record/list_modified/text()}</span>,<br/>,
  <strong>Date created: </strong>,<span>{$record/list_created/text()}</span>,<br/>,

  if ($std != "")
  then (
    <strong>Part of TDWG Standard: </strong>,<a href='{$std}'>{$std}</a>,<br/>
    )
  else (
    <span>Not part of any TDWG Standard</span>,<br/>
    ),
  
  <strong>This version: </strong>,<a href='{$thisVersion}'>{$thisVersion}</a>,<br/>,
  <strong>Latest version: </strong>,<a href='{$record/list/text()}'>{$record/list/text()}</a>,<br/>,
  <strong>Abstract: </strong>,<span>{$record/description/text()}</span>,<br/>,
  
  if ($record/vann_preferredNamespacePrefix/text() != "")
  then (
    <strong>Namespace IRI: </strong>,<span>{$record/vann_preferredNamespaceUri/text()}</span>,<br/>,
    <strong>Preferred namespace abbreviation: </strong>,<span>{$record/vann_preferredNamespacePrefix/text()||":"}</span>,<br/>
    )
  else (),
  
  if ($record/list_deprecated/text() = "true")
  then (
    <strong>Status note: </strong>,<span>This term list has been deprecated and is no longer recommended for use.</span>,<br/>
    )
  else (),
  <br/>
  
}</div>
};

(: Generates the HTML for the middle section of the term list page and returns it as a div elelment :)
declare function html:generate-list-toc-etc-html($termListIri as xs:string) as element()
{
<div>
  <h1>Table of Contents</h1>
  <ul style="list-style: none;">
    <li><a href="#1">1 Introduction</a></li>
    <li><a href="#2">2 List versions</a></li>
    <li><a href="#3">3 List distributions</a></li>
    <li><a href="#4">4 Terms that are members of this list</a></li>
  </ul>
  <h1><a id="1">1 Introduction</a></h1>
  <p>This is a list of terms that may be part of a TDWG vocabulary.  If the terms on this list are defined by TDWG, the list corresponds to terms in a namespace whose IRI is listed in the header.  In the case where the terms are borrowed from a non-TDWG vocabulary, the list includes terms that are &quot;borrowed&quot; for inclusion in a TDWG vocabulary.  The list includes all &quot;current&quot; terms on the list, which may or may not be recommended for use.  Terms that are no longer recommended for use may have specified replacements - see the metadata about that specific term.</p>
  <p>For more information about the structure and version model of TDWG vocabularies, see the <a href="http://www.tdwg.org/standards/147">TDWG Standards Documentation Specification</a>.</p>
  <h1><a id="2">2 List versions</a></h1>
  <p>List versions are &quot;snapshots&quot; of the term list at a particular point in time. To examine specific historical versions of this list, click on one of the links below.</p>
  <ul style="list-style: none;">{
    let $listRaw := html:generateLinkedMetadata("term-lists")
    let $versions := $listRaw/metadata/record  
    for $version in $versions
    where $version/list/text() = $termListIri
    return <li><a href="{$version/version/text()}">{$version/version/text()}</a></li>
  }</ul>
  <h1><a id="3">3 List distributions</a></h1>
  <p>This term list is available in the formats or distribution methods listed in the table below.  Please note that distribution access URLs may be subject to change over time.  Therefore, it is preferable to request the abstract IRI of the resources and request the desired Content-type through content negotiation.</p>
  <table border="1">{
    let $iri := html:substring-before-last($termListIri,"/")
    return (
    <tr><th>Description</th><th>IRI</th><th>Access URL</th></tr>,
    <tr><td>HTML file (this document)</td><td>{$iri||".htm"}</td><td><a href="{$iri||'.htm'}">{$iri||".htm"}</a></td></tr>,
    <tr><td>RDF/Turtle</td><td>{$iri||".ttl"}</td><td><a href="{$iri||'.ttl'}">{$iri||".ttl"}</a></td></tr>,
    <tr><td>RDF/XML</td><td>{$iri||".rdf"}</td><td><a href="{$iri||'.rdf'}">{$iri||".rdf"}</a></td></tr>,
    <tr><td>JSON-LD</td><td>{$iri||".json"}</td><td><a href="{$iri||'.json'}">{$iri||".json"}</a></td></tr>
    )
  }</table>
  <h1><a id="4">4 Terms that are members of this list</a></h1>
</div>
};

(: Generate the HTML tables of metadata about the terms in the list and returns them as a div element :)
declare function html:generate-list-html($db as xs:string,$ns as xs:string) as element()
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)

let $coreDoc := $config/coreClassFile/text()
let $metadataSeparator := $config/separator/text()
let $metadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

let $linkedMetadataRaw := html:generateLinkedMetadata($db)
let $linkedMetadata := $linkedMetadataRaw/metadata/record
  
return 
     <div>
       {
       for $record in $metadata
       let $localName := $record/term_localName/text()
       let $version := html:most-recent-version($linkedMetadata,$localName)[last()]
       order by $localName
       return (
         html:term-metadata($record,$version,$linkedMetadata,$ns),<br/>
         )
       }
     </div>
};

(:--------------------------------------------------------------------------------------------------:)
(: Generate term list versions web page ////////////////////////////////////////////////////////////////////:)
(:--------------------------------------------------------------------------------------------------:)

(: 1st level function :)

(: Generates web page for term lists versions; usually following the pattern http://rs.tdwg.org/{vocab}/version/{term-list}/{iso-date} :)
declare function html:generate-term-list-version-html($termListVersionIri as xs:string) as element()
{
let $listMetadata := html:load-metadata-record($termListVersionIri,"term-lists-versions")
let $versionRoot := html:substring-before-last($termListVersionIri,"/") (: find the part of the version before the ISO 8601 date :)
let $termListIri := replace($versionRoot,'version/','')||"/"
let $ns := html:find-list-ns-abbreviation($termListIri)
let $std := html:find-standard-for-list($termListIri)
let $members := html:generate-list-version-members($termListVersionIri)
return
<html>
  <head>
    <meta charset="utf-8"/>
    <title>{$listMetadata/label/text()||" "||$listMetadata/version_modified/text()||" version"}</title>
  </head>
  <body>{
    html:generate-list-versions-metadata-html($listMetadata,$std,$termListIri),
    html:generate-list-versions-toc-etc-html($termListVersionIri),
    html:generate-list-versions-html(html:find-list-version-dbname($termListIri),$ns,$members),
    html:generate-footer()
   }</body>
</html>
};

(:--------------------------------------------------------------------------------------------------:)
(: 2nd level functions :)

(: Generates metadata for a list version and returns it as an HTML div element :)
declare function html:generate-list-versions-metadata-html($record as element(),$std as xs:string,$termListIri as xs:string) as element()
{
let $linkedMetadataRaw := html:generateLinkedMetadata("term-lists-versions")
let $replacements := $linkedMetadataRaw/metadata/record
(: let $replacements := fn:collection("term-lists-versions")/linked-metadata/file/metadata/record :)
return
<div>{
  <strong>Title: </strong>,<span>{$record/label/text()||" (version)"}</span>,<br/>,
  <strong>Issued: </strong>,<span>{$record/version_modified/text()}</span>,<br/>,

  if ($std != "")
  then (
    <strong>Part of TDWG Standard: </strong>,<a href='{$std}'>{$std}</a>,<br/>
    )
  else (
    <span>Not part of any TDWG Standard</span>,<br/>
    ),
  
  <strong>This version: </strong>,<a href='{$record/version/text()}'>{$record/version/text()}</a>,<br/>,
  <strong>Version status: </strong>,<span>{$record/status/text()}</span>,<br/>,
  <strong>Latest version: </strong>,<a href='{$termListIri}'>{$termListIri}</a>,<br/>,
  
  for $replacement in $replacements
  where $replacement/replacing_list/text() = $record/version/text()
  return (<strong>Previous version:</strong>,<a href='{$replacement/replaced_list/text()}'>{$replacement/replaced_list/text()}</a>,<br/>),

  for $replacement in $replacements
  where $replacement/replaced_list/text() = $record/version/text()
  return (<strong>Replaced by:</strong>,<a href='{$replacement/replacing_list/text()}'>{$replacement/replacing_list/text()}</a>,<br/>),

  <strong>Abstract: </strong>,<span>This version lists the member terms on the date that the list was issued.  The status shown for the term version is its current status.</span>,<br/>,
  
  if ($record/vann_preferredNamespacePrefix/text() != "")
  then (
    <strong>Namespace IRI: </strong>,<span>{$record/vann_preferredNamespaceUri/text()}</span>,<br/>,
    <strong>Preferred namespace abbreviation: </strong>,<span>{$record/vann_preferredNamespacePrefix/text()||":"}</span>,<br/>
    )
  else (),
  
  if ($record/list_deprecated/text() = "true")
  then (
    <strong>Status note: </strong>,<span>This term list has been deprecated and is no longer recommended for use.</span>,<br/>
    )
  else (),
  <br/>
  
}</div>
};

(: Generates the HTML for the middle section of the term list versions page and returns it as a div elelment :)
declare function html:generate-list-versions-toc-etc-html($termListVersionIri as xs:string) as element()
{
<div>
  <h1>Table of Contents</h1>
  <ul style="list-style: none;">
    <li><a href="#1">1 Introduction</a></li>
    <li><a href="#2">2 List version distributions</a></li>
    <li><a href="#3">3 Term versions that were members of this list when this version of it was issued</a></li>
  </ul>
  <h1><a id="1">1 Introduction</a></h1>
  <p>This is a list of term versions that may be part of a TDWG vocabulary.  If the terms whose versions are on this list were defined by TDWG, the list corresponds to term versions in a namespace whose IRI is listed in the header.  In the case where the terms were borrowed from a non-TDWG vocabulary, the list includes term versions that were &quot;borrowed&quot; for inclusion in a TDWG vocabulary.</p>
  <p>This list includes term versions that were part of the term list at the time this version was issued.  The status of the individual terms may have changed since the version was issued.  The version status indicates its status at the present time, not at the time the list version was issued.</p>
  <p>For more information about the structure and version model of TDWG vocabularies, see the <a href="http://www.tdwg.org/standards/147">TDWG Standards Documentation Specification</a>.</p>
  <h1><a id="2">2 List version distributions</a></h1>
  <p>This term versions list is available in the formats or distribution methods listed in the table below.  Please note that distribution access URLs may be subject to change over time.  Therefore, it is preferable to request the abstract IRI of the resources and request the desired Content-type through content negotiation.</p>
  <table border="1">{
    let $iri := $termListVersionIri
    return (
    <tr><th>Description</th><th>IRI</th><th>Access URL</th></tr>,
    <tr><td>HTML file (this document)</td><td>{$iri||".htm"}</td><td><a href="{$iri||'.htm'}">{$iri||".htm"}</a></td></tr>,
    <tr><td>RDF/Turtle</td><td>{$iri||".ttl"}</td><td><a href="{$iri||'.ttl'}">{$iri||".ttl"}</a></td></tr>,
    <tr><td>RDF/XML</td><td>{$iri||".rdf"}</td><td><a href="{$iri||'.rdf'}">{$iri||".rdf"}</a></td></tr>,
    <tr><td>JSON-LD</td><td>{$iri||".json"}</td><td><a href="{$iri||'.json'}">{$iri||".json"}</a></td></tr>
    )
  }</table>
  <h1><a id="3">3 Term versions that were members of this list when this version of it was issued</a></h1>
</div>
};

(: Generate the HTML table of metadata about the terms in the list:)
declare function html:generate-list-versions-html($db as xs:string,$ns as xs:string,$members as xs:string+) as element()
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)

let $coreDoc := $config/coreClassFile/text()
let $metadataSeparator := $config/separator/text()
let $metadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

let $linkedMetadataRaw := html:generateLinkedMetadata($db)
let $replacements := $linkedMetadataRaw/metadata/record
return 
     <div>
       {
       for $record in $metadata, $member in $members
       where $record/version/text()=$member
       order by $record/term_localName/text()
       let $versionRoot := substring($record/version/text(),1,
fn:string-length($record/version/text())-11) (: find the part of the version before the ISO 8601 date :)
       let $versionOf := replace($versionRoot,'version/','')
       return (
         html:term-version-metadata($record,$versionOf,$replacements,$ns),
         <br/>
         )
       }
     </div>
};

(:--------------------------------------------------------------------------------------------------:)
(: defunct test functions :)

(: This is the test template web page for the /home URI pattern :)
declare function html:generate-list($db)
{
let $repoPath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||html:branch()||"/"
let $config := html:load-configuration($repoPath, $db)

let $coreDoc := $config/coreClassFile/text()
let $metadataSeparator := $config/separator/text()
let $baseIriColumn := $config/baseIriColumn/text()

let $metadataDoc := http:send-request(<http:request method='get' href='{$repoPath||$db||"/"||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record
  
return 
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Test</title>
      <link href="https://raw.githubusercontent.com/baskaufs/tdwg-standards/master/html/config/default.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
     <table cellspacing="0" class="border">
       <tbody>
       <!-- Begin Terms Table -->
       {
       for $record in $metadata
       return (
         <tr><th colspan="2"><a name="{$record/term_localName/text()}">Term Name: {$record/label/text()}</a></th></tr>,
         <tr><td>Identifier:</td><td>{$record/term_isDefinedBy/text()||$record/term_localName/text()}</td></tr>,
         <tr><td>Class:</td><td>{$record/dwcattributes_organizedInClass/text()}</td></tr>,
         <tr><td>Definition:</td><td>{$record/rdfs_comment/text()}</td></tr>,
         <tr><td>Comment:</td><td>{$record/dcterms_description/text()||" For discussion see "}<a href="{'http://terms.tdwg.org/wiki/dwc:'||$record/term_localName/text()}">{'http://terms.tdwg.org/wiki/dwc:'||$record/term_localName/text()}</a></td></tr>,
         <tr><td>Details:</td><td><a href="{$record/version/text()}">{$record/term_localName/text()}</a></td></tr>
         )
       }
       </tbody>
     </table>
  </body>
</html>
};

declare function html:term-lists-versions($lookup-string as xs:string) as element()
{
};
