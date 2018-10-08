(: this module needs to be put in the webapp folder of your BaseX installation.  On my local computer it's at c:\Program Files (x86)\BaseX\webapp\ On the Tomcat installation, it's at opt/tomcat/webapps/gom/restxq.xqm, where gom is the context under which the BaseX server is running :)

module namespace page = 'http://basex.org/modules/web-page';
import module namespace serialize = 'http://bioimages.vanderbilt.edu/xqm/serialize' at 'https://raw.githubusercontent.com/baskaufs/guid-o-matic/master/serialize.xqm';
import module namespace html = 'http://rs.tdwg.com/html' at 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/html/html.xqm';
(: import module namespace html = 'http://rs.tdwg.com/html' at 'https://raw.githubusercontent.com/baskaufs/msc/master/tdwg-metadata-reference/html/html.xqm'; :)

(:----------------------------------------------------------------------------------------------:)
(: Main functions for handling URI patterns :)

(: This is a test function for testing the kind of Accept header sent by the client :)
declare
  %rest:path("/header")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:web($acceptHeader)
  {
  <p>{$acceptHeader}</p>
  };

(: This is a function to provide an option to dump an entire dataset :)
declare
  %rest:path("/dump/{$db}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dump($acceptHeader,$db)
  {
    (: $db is the Github database to be dumped as RDF :)
  let $ext := page:determine-extension($acceptHeader)
  let $extension :=
      if ($ext = "htm")
      then
          (: If the client is a browser, return Turtle :)
          "ttl"
      else
          (: Otherwise, return the requested media type :)
          $ext
  let $response-media-type := page:determine-media-type($extension)
  let $flag := page:determine-type-flag($extension)

  return
      (
      <rest:response>
        <output:serialization-parameters>
          <output:media-type value='{$response-media-type}'/>
        </output:serialization-parameters>
      </rest:response>,
      serialize:main-github("",$flag,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/",$db,"dump","false")
      )
  };

(: Handler for the special URI pattern for Executive Committee decision instances under the "/decisions/" subpath :)
declare
  %rest:path("/decisions/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:decisions($acceptHeader,$local-id)
  {
  page:generic-simple-id($local-id,"decisions",$acceptHeader)
  };

(: This is the handler function for URI patterns of "/{vocab}/" (vocabularies):)
declare
  %rest:path("/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-vocabularies($acceptHeader,$local-id)
  {
  let $db := "vocabularies"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($local-id,".")
      let $extension := substring-after($local-id,".")

      let $lookup-string := "http://rs.tdwg.org/"||$stripped-local-name||"/"
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/"||$local-id||"/"
      let $redirect-id := "/"||$local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: This is the handler function for URI patterns of "/{vocab}/doc/{docname}/" (standards documents) :)
declare
  %rest:path("/{$vocab}/doc/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-docs($acceptHeader,$vocab,$local-id)
  {
  let $db := "docs"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($local-id,".")
      let $extension := substring-after($local-id,".")
      let $lookup-string := "http://rs.tdwg.org/"||$vocab||"/doc/"||$stripped-local-name||"/"
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/"||$vocab||"/doc/"||$local-id||"/"
      let $redirect-id := "/"||$vocab||"/doc/"||$local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handler for URI patterns where the local name follows the "/{vocab}/{namespace}/" subpath (generic terms) :)
declare
  %rest:path("/{$vocab}/{$ns}/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:generic-terms($acceptHeader,$vocab,$ns,$local-id)
  {
  let $listLocalname := $vocab||"/"||$ns||"/"
  let $termlistFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/term-lists/term-lists.csv"
  let $termlistDoc := http:send-request(<http:request method='get' href='{$termlistFilePath}'/>)[2]
  let $termlistDataRaw := csv:parse($termlistDoc, map { 'header' : true(),'separator' : "," })
  let $termlistData := $termlistDataRaw/csv/record

  for $termlist in $termlistData
  where $termlist/list_localName/text() = $listLocalname
  return page:generic-simple-id($local-id,$termlist/database/text(),$acceptHeader)
  };

(: Handler for the special URI pattern for tdwgutility: terms under the "/dwc/terms/attributes/" subpath (generic terms) :)
declare
  %rest:path("/dwc/terms/attributes/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:tdwgutility-terms($acceptHeader,$local-id)
  {
  page:generic-simple-id($local-id,"utility",$acceptHeader)
  };

(: Handler for the special URI pattern for tdwgutility: term versions under the "/dwc/terms/attributes/version/" subpath (generic terms) :)
declare
  %rest:path("/dwc/terms/attributes/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:tdwgutility-term-versions($acceptHeader,$local-id)
  {
  page:generic-simple-id($local-id,"utility-versions",$acceptHeader)
  };

(: Handler for URI patterns where the local name follows the "/ac/terms/" subpath (Audubon Core-defined terms) :)
(:
  declare
  %rest:path("/ac/terms/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:audubon($acceptHeader,$local-id)
  {
  let $db := "audubon"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)

(: Handler for URI patterns where the local name follows the "/{vocab}/{namespace}/version/" subpath (generic term versions) :)
declare
  %rest:path("/{$vocab}/{$ns}/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:generic-term-version($acceptHeader,$vocab,$ns,$local-id)
  {
  let $listLocalname := $vocab||"/"||$ns||"/"
  let $termlistFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/term-lists/term-lists.csv"
  let $termlistDoc := http:send-request(<http:request method='get' href='{$termlistFilePath}'/>)[2]
  let $termlistDataRaw := csv:parse($termlistDoc, map { 'header' : true(),'separator' : "," })
  let $termlistData := $termlistDataRaw/csv/record

  for $termlist in $termlistData
  where $termlist/list_localName/text() = $listLocalname
  return page:generic-simple-id($local-id,$termlist/database/text()||"-versions",$acceptHeader)

  };

(: Handler for URI patterns where the local name follows the "/ac/terms/version/" subpath (Audubon Core) :)
(:
declare
  %rest:path("/ac/terms/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:audubon-versions($acceptHeader,$local-id)
  {
  let $db := "audubon-versions"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/curatorial/" subpath :)
(:
declare
  %rest:path("/dwc/curatorial/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-curatorial($acceptHeader,$local-id)
  {
  let $db := "curatorial"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/curatorial/version/" subpath :)
(:
declare
  %rest:path("/dwc/curatorial/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:curatorial-versions($acceptHeader,$local-id)
  {
  let $db := "curatorial-versions"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/dwcore/" subpath :)
(:
declare
  %rest:path("/dwc/dwcore/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-dwcore($acceptHeader,$local-id)
  {
  let $db := "dwcore"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/dwcore/version/" subpath :)
(:
declare
  %rest:path("/dwc/dwcore/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwcore-versions($acceptHeader,$local-id)
  {
  let $db := "dwcore-versions"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/dwctype/" subpath (DwC type vocabulary :)
(:
declare
  %rest:path("/dwc/dwctype/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-dwctype($acceptHeader,$local-id)
  {
  let $db := "dwctype"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/dwctype/version/" subpath (DwC type vocab) :)
(:
declare
  %rest:path("/dwc/dwctype/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwctype-versions($acceptHeader,$local-id)
  {
  let $db := "dwctype-versions"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/geospatial/" subpath :)
(:
declare
  %rest:path("/dwc/geospatial/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-geospatial($acceptHeader,$local-id)
  {
  let $db := "geospatial"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/geospatial/version/" subpath :)
(:
declare
  %rest:path("/dwc/geospatial/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:geospatial-versions($acceptHeader,$local-id)
  {
  let $db := "geospatial-versions"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/iri/" subpath (dwciri: terms) :)
(:
declare
  %rest:path("/dwc/iri/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:iri($acceptHeader,$local-id)
  {
  let $db := "iri"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/dwc/iri/version/" subpath (dwciri: term versions) :)
(:
declare
  %rest:path("/dwc/iri/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:iri-versions($acceptHeader,$local-id)
  {
  let $db := "iri-versions"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Special handler for URI patterns where a final string follows the "/dwc/terms/" subpath (Darwin Core terms and Utility term list :)
(: Note: This must be hard-coded. Although the dwc: terms could be handled by the generic terms handler, there is no way to get the non-fixed :)
(: extension from the /dwc/terms/attributes local name without using the {$local-id} pattern matching.  :)
declare
  %rest:path("/dwc/terms/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-terms($acceptHeader,$local-id)
  {
  let $db := "terms"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $extension := substring-after($local-id,".")
      let $lookup-string := substring-before($local-id,".")
      return if ($lookup-string = "attributes")
             then
               (: handle the special case of the tdwgutility: term list "/dwc/terms/attributes/". :)
               page:handle-repesentation($acceptHeader,$extension,"term-lists","http://rs.tdwg.org/dwc/terms/attributes/")
             else
               page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := $local-id
      let $redirect-id := $local-id
      return if ($lookup-string = "attributes")
             then
               (: handle the special case of the tdwgutility: term list "/dwc/terms/attributes/". :)
               page:see-also($acceptHeader,"/dwc/terms/attributes","term-lists","http://rs.tdwg.org/dwc/terms/attributes/")
             else
               page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handler for URI patterns where the local name follows the "/dwc/terms/version/" subpath (Darwin Core term versions) :)
(:
declare
  %rest:path("/dwc/terms/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:terms-versions($acceptHeader,$local-id)
  {
  let $db := "terms-versions"
  return page:generic-simple-id($local-id,$db,$acceptHeader)
  };
:)
(: Handler for URI patterns where the local name follows the "/version/{vocab}/" subpath (vocabulary versions) :)
declare
  %rest:path("/version/{$vocab}/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-vocabularies-versions($acceptHeader,$vocab,$local-id)
  {
  let $db := "vocabularies-versions"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($local-id,".")
      let $extension := substring-after($local-id,".")
      let $lookup-string := "http://rs.tdwg.org/version/"||$vocab||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/version/"||$vocab||"/"||$local-id
      let $redirect-id := "/version/"||$vocab||"/"||$local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handler for URI patterns of "/{vocab}/{list}/" (term lists) :)
declare
  %rest:path("/{$namespace}/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-term-lists($acceptHeader,$namespace,$local-id)
  {
  let $db := "term-lists"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($local-id,".")
      let $extension := substring-after($local-id,".")
      let $lookup-string := "http://rs.tdwg.org/"||$namespace||"/"||$stripped-local-name||"/"
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/"||$namespace||"/"||$local-id||"/"
      let $redirect-id := "/"||$namespace||"/"||$local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handler for URI patterns where the local name follows the "/{vocab}/version/{list}/" subpath (term list versions) :)
declare
  %rest:path("/{$vocab}/version/{$term-list}/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-term-lists-versions($acceptHeader,$vocab,$term-list,$local-id)
  {
  let $db := "term-lists-versions"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($local-id,".")
      let $extension := substring-after($local-id,".")
      let $lookup-string := "http://rs.tdwg.org/"||$vocab||"/version/"||$term-list||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/"||$vocab||"/version/"||$term-list||"/"||$local-id
      let $redirect-id := $local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Ideosyncratic redirects to fixed categories of resources :)
(: See documentation at http://docs.basex.org/wiki/RESTXQ#Forwards_and_Redirects :)
(: 302 redirects :)

(: Tapir redirects :)
declare %rest:path("/tapir/cns/{$path=.+}") function page:tapir-cns-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/tapir/cns/"||$path}</rest:redirect>};

declare %rest:path("/tapir/cs/{$path=.+}") function page:tapir-cs-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/tapir/cs/"||$path}</rest:redirect>};

declare %rest:path("/tapir/1.0/schema/tdwg_tapir.xsd") function page:tapir10-schema-redirect()
 {<rest:redirect>{"https://raw.githubusercontent.com/tdwg/tapir/1.0/schema/tapir.xsd"}</rest:redirect>};

declare %rest:path("/tapir/1.0/{$path=.+}") function page:tapir10-redirect($path)
 {<rest:redirect>{"https://raw.githubusercontent.com/tdwg/tapir/1.0/"||$path}</rest:redirect>};

(: TDWG ontology redirects :)
declare %rest:path("/ontology/{$path=.+}") function page:ontology-redirect($path)
  {<rest:redirect>{"http://tdwg.github.io/ontology/ontology/"||$path}</rest:redirect>};

declare %rest:path("/ontology2/{$path=.+}") function page:ontology2-redirect($path)
  {<rest:redirect>{"http://tdwg-ontology.googlecode.com/svn/trunk/ontology/"||$path}</rest:redirect>};

(: SDD redirects :)
declare %rest:path("/UBIF/{$path=.+}") function page:ubif-forward($path)
  {<rest:redirect>{"http://tdwg.github.io/sdd/"||$path}</rest:redirect>};

declare %rest:path("/sdd/{$path=.+}") function page:sdd-forward($path)
  {<rest:redirect>{"http://tdwg.github.io/sdd/"||$path}</rest:redirect>};

(: ABCD redirects :)
declare %rest:path("/abcd2/terms/{$path=.+}") function page:abdc2-redirect($path)
  {<rest:redirect>{"http://terms.tdwg.org/wiki/abcd2:"||$path}</rest:redirect>};

declare %rest:path("/abcd-efg/terms/{$path=.+}") function page:abdcefg-redirect($path)
  {<rest:redirect>{"http://terms.tdwg.org/wiki/abcd-efg:"||$path}</rest:redirect>};

declare %rest:path("/abcd/{$path=.+}") function page:abdc-redirect($path)
  {<rest:redirect>{"http://tdwg.github.io/abcd/"||$path}</rest:redirect>};

(: Darwin Core generic redirects when specific content negotiation doesn't kick in :)
(: must have subpath to not override the vocabulary terms :)
declare %rest:path("/dwc/xsd/{$path=.+}") function page:dwc-xsd-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/dwc/xsd/"||$path}</rest:redirect>};

declare %rest:path("/dwc/text/{$path=.+}") function page:dwc-text-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/dwc/text/"||$path}</rest:redirect>};

declare %rest:path("/dwc/rdf/{$path=.+}") function page:dwc-rdf-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/dwc/rdf/"||$path}</rest:redirect>};

declare %rest:path("/dwc/downloads/{$path=.+}") function page:dwc-downloads-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/dwc/downloads/"||$path}</rest:redirect>};

declare %rest:path("/dwc/examples/{$path=.+}") function page:dwc-examples-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/dwc/rexamples/"||$path}</rest:redirect>};

declare %rest:path("/dwc/DarwinCore_files/{$path=.+}") function page:dwc-files-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/dwc/DarwinCore_files/"||$path}</rest:redirect>};

declare %rest:path("/dwc/index_legacy_rddl.html") function page:tdwg-legacy-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/index_legacy_rddl.html"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_basetypes.xsd") function page:tdwg-basetypes-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_basetypes.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_core.xsd") function page:tdwg-dw-core-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_dw_core.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_curatorial.xsd") function page:tdwg-dw-curat-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_dw_curatorial.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_element.xsd") function page:tdwg-dw-element-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_dw_element.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_geospatial.xsd") function page:tdwg-dw-geo-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_dw_geospatial.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_record.xsd") function page:tdwg-dw-record-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_dw_record.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_record_tapir.xsd") function page:tdwg-dw-tapir-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_dw_record_tapir.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_gml.xsd") function page:tdwg-gml-redirect()
 {<rest:redirect>{"https://tdwg.github.io/dwc/tdwg_gml.xsd"}</rest:redirect>};


(:----------------------------------------------------------------------------------------------:)
(: Second-level functions :)

(: Generic handler for simple local IDs :)
declare function page:generic-simple-id($local-id,$db,$acceptHeader)
{
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $extension := substring-after($local-id,".")
      let $lookup-string := substring-before($local-id,".")
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := $local-id
      let $redirect-id := $local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
};

(: Handle request for specific representation when requested with file extension :)
declare function page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
{
  if (serialize:find-github($lookup-string,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/",$db))  (: check whether the resource is in the database :)
  then
    (: When a specific file extension is requested, override the requested content type. :)
    let $response-media-type := page:determine-media-type($extension)
    let $flag := page:determine-type-flag($extension)
    return page:return-representation($response-media-type,$lookup-string,$flag,$db)
  else
    page:not-found()  (: respond with 404 if not in database :)
};

(: Function to return a representation of a resource :)
declare function page:return-representation($response-media-type,$lookup-string,$flag,$db)
{
  if ($flag = "html")
  then if ($db = "docs")
      then page:handle-docs-html($lookup-string)
      else page:handle-html($db,$lookup-string)
  else
  (: I moved this within the ELSE statement because it interferes with the HTML redirect if I leave it before the IF :)
  <rest:response>
    <output:serialization-parameters>
      <output:media-type value='{$response-media-type}'/>
    </output:serialization-parameters>
  </rest:response>,
  serialize:main-github($lookup-string,$flag,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/",$db,"single","false")
};

(: Function to return a web page for vocabs etc. :)
declare function page:handle-html($db,$lookup-string)
{
let $redirectFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/html/redirects.csv"
let $redirectDoc := http:send-request(<http:request method='get' href='{$redirectFilePath}'/>)[2]
let $redirectDataRaw := csv:parse($redirectDoc, map { 'header' : true(),'separator' : "," })
let $redirectData := $redirectDataRaw/csv/record
for $redirectItem in $redirectData
where $redirectItem/database/text() = $db
return
  if ($redirectItem/redirect/text() = "no")
  then
    switch ($redirectItem/type/text())
      case "term" return (page:success(),html:generate-term-html($db,$redirectItem/namespace/text(),$lookup-string))
      case "termVersion" return (page:success(),html:generate-term-version-html($db,$redirectItem/namespace/text(),$lookup-string))
      case "termList" return (page:success(),html:generate-term-list-html($lookup-string))
      case "termListVersion" return (page:success(),html:generate-term-list-version-html($lookup-string))
      case "vocabulary" return (page:success(),html:generate-vocabulary-html($lookup-string))
      case "vocabularyVersion" return (page:success(),html:generate-vocabulary-version-html($lookup-string))
      default return page:not-found()
  else
    (: this sort of redirect only makes sense for terms and term versions :)
    let $base :=
      if ($redirectItem/useNamespace/text()="yes")
      then $redirectItem/prefix/text()||$redirectItem/namespace/text()||$redirectItem/connector/text()
      else $redirectItem/prefix/text()
    return page:temp-redirect($base,$lookup-string)

(:
  switch ($db)
   case "audubon" return page:temp-redirect("https://terms.tdwg.org/wiki/Audubon_Core_Term_List#ac:",$lookup-string)
   case "audubon-versions" return (page:success(),html:generate-term-version-html($db,"ac",$lookup-string))
   case "curatorial" return (page:success(),html:generate-term-html($db,"dwccuratorial",$lookup-string))
   case "curatorial-versions" return (page:success(),html:generate-term-version-html($db,"dwccuratorial",$lookup-string))
   case "dwcore" return (page:success(),html:generate-term-html($db,"dwcore",$lookup-string))
   case "dwcore-versions" return (page:success(),html:generate-term-version-html($db,"dwcore",$lookup-string))
   case "dwctype" return (page:success(),html:generate-term-html($db,"dwctype",$lookup-string))
   case "dwctype-versions" return (page:success(),html:generate-term-version-html($db,"dwctype",$lookup-string))
   case "geospatial" return (page:success(),html:generate-term-html($db,"dwcgeospatial",$lookup-string))
   case "geospatial-versions" return (page:success(),html:generate-term-version-html($db,"dwcgeospatial",$lookup-string))
   case "iri" return (page:success(),html:generate-term-html($db,"dwciri",$lookup-string))
   case "iri-versions" return (page:success(),html:generate-term-version-html($db,"dwciri",$lookup-string))
   case "terms" return page:temp-redirect("http://rs.tdwg.org/dwc/terms/#",$lookup-string)
   case "terms-versions" return (page:success(),html:generate-term-version-html($db,"dwc",$lookup-string))
   case "term-lists" return (page:success(),html:generate-term-list-html($lookup-string))
   case "term-lists-versions" return (page:success(),html:generate-term-list-version-html($lookup-string))
   case "vocabularies" return (page:success(),html:generate-vocabulary-html($lookup-string))
   case "vocabularies-versions" return (page:success(),html:generate-vocabulary-version-html($lookup-string))
   default return <p>database handler not yet written</p>
   :)
};

(: Function to redirect to a web page for standards documents :)
declare function page:handle-docs-html($lookup-string)
{
let $redirectFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/docs/docs.csv"
let $redirectDoc := http:send-request(<http:request method='get' href='{$redirectFilePath}'/>)[2]
let $redirectDataRaw := csv:parse($redirectDoc, map { 'header' : true(),'separator' : "," })
let $redirectData := $redirectDataRaw/csv/record
for $redirectItem in $redirectData
where $redirectItem/current_iri/text() = $lookup-string
return page:temp-redirect($redirectItem/browserRedirectUri/text(),"")
};

(: 200 Success response:)
declare function page:success()
{
  <rest:response>
    <http:response status="200" message="Success">
      <http:header name="Content-Language" value="en"/>
      <http:header name="Content-Type" value="text/html; charset=utf-8"/>
    </http:response>
  </rest:response>
};

(: 302 "temporary" redirect with local name appended to end of a base URI :)
declare function page:temp-redirect($base,$local-id)
{
  <rest:response>
    <http:response status="302">
      <http:header name="location" value="{$base||$local-id}"/>
    </http:response>
  </rest:response>
};

(: 303 See Also redirect to specific representation having file exension, based on requested media type :)
declare function page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
{
  if(serialize:find-github($lookup-string,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/",$db))  (: check whether the resource is in the database :)
  then
      let $extension := page:determine-extension($acceptHeader)
      return
          <rest:response>
            <http:response status="303">
              <http:header name="location" value="{ concat($redirect-id,".",$extension) }"/>
            </http:response>
          </rest:response>
  else
      page:not-found() (: respond with 404 if not in database :)
};

(: Function to generate a 404 Not found response :)
declare function page:not-found()
{
  <rest:response>
    <http:response status="404" message="Not found.">
      <http:header name="Content-Language" value="en"/>
      <http:header name="Content-Type" value="text/html; charset=utf-8"/>
    </http:response>
  </rest:response>
};

(:----------------------------------------------------------------------------------------------:)
(: Utility functions to set media type-dependent values :)

(: Functions used to set media type-specific values :)
declare function page:determine-extension($header)
{
  if (contains(string-join($header),"application/rdf+xml"))
  then "rdf"
  else
      if (contains(string-join($header),"text/turtle"))
      then "ttl"
      else
          if (contains(string-join($header),"application/ld+json") or contains(string-join($header),"application/json"))
          then "json"
          else "htm"
};

declare function page:determine-media-type($extension)
{
  switch($extension)
    case "rdf" return "application/rdf+xml"
    case "ttl" return "text/turtle"
    case "json" return "application/ld+json"
    default return "text/html"
};

declare function page:determine-type-flag($extension)
{
  switch($extension)
    case "rdf" return "xml"
    case "ttl" return "turtle"
    case "json" return "json"
    default return "html"
};
