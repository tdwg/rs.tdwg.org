(: this module needs to be put in the webapp folder of your BaseX installation.  On my local computer it's at c:\Program Files (x86)\BaseX\webapp\ On the Tomcat installation, it's at opt/tomcat/webapps/gom/restxq.xqm, where gom is the context under which the BaseX server is running :)

module namespace page = 'http://basex.org/modules/web-page';
import module namespace html = 'http://rs.tdwg.com/html' at 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/html/html.xqm';

(:----------------------------------------------------------------------------------------------:)
(: Main functions for handling URI patterns :)

(: Miscellaneous patterns :)

(: root pattern. Note: this just redirects to /index :)
declare
  %rest:path("/")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:root($acceptHeader)
  {
  page:see-also($acceptHeader,"/index","index","http://rs.tdwg.org/index")
  };

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
  (: $db is the database to be dumped as RDF :)
  if (contains($db,"."))
  then
      (: The database name has an extension, so deliver it :)
      let $stripped-local-name := substring-before($db,".")
      let $extension := substring-after($db,".")
      return
      if (page:check-db($stripped-local-name))
      then
          if ($extension = "htm")
          then
              (: html requested by browser or .htm explicitly requested :)
              <rest:redirect>{"https://github.com/tdwg/rs.tdwg.org/tree/master/"||$stripped-local-name}</rest:redirect>
          else
              (: respond with correct content-type header for dump of requested media type:)
              let $response-media-type := page:determine-media-type($extension)
              let $flag := page:determine-type-flag($extension)
              return
                  (
                  <rest:response>
                    <output:serialization-parameters>
                      <output:media-type value='{$response-media-type}'/>
                    </output:serialization-parameters>
                  </rest:response>,
                  page:main-db("",$flag,"dump",$stripped-local-name)
                  )
      else page:not-found()
  else
      (: The database name has no extension, so perform content negotiation :)
      if (page:check-db($db))
      then
          let $extension := page:determine-extension($acceptHeader)
          return
              <rest:response>
                <http:response status="303">
                  <http:header name="location" value="{'/dump/'||$db||'.'||$extension}"/>
                </http:response>
              </rest:response>
      else page:not-found()
  };

declare function page:check-db($db)
{
  let $metadataDoc := http:send-request(<http:request method='get' href='{"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/index/index-datasets.csv"}'/>)[2]
  let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : ',' })
  let $metadata := $xmlMetadata/csv/record
  for $record in $metadata
  where $record/term_localName/text()=$db
  return true()
};

(: Handler for the special URI pattern for Executive Committee decision instances under the "/decisions/" subpath :)
declare
  %rest:path("/decisions/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:decisions($acceptHeader,$local-id)
  {
  page:generic-simple-id($local-id,"decisions",$acceptHeader)
  };

(:----------------------------------------------------------------------------------------------:)
(: Document patterns :)

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

(: This is the handler function for URI patterns of "/{vocab}/doc/{docname}/{versionDate}" (standards documents versions) :)
declare
  %rest:path("/{$vocab}/doc/{$local-id}/{$date}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-docs-versions($acceptHeader,$vocab,$local-id,$date)
  {
  let $db := "docs-versions"
  return
    if (contains($date,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($date,".")
      let $extension := substring-after($date,".")
      let $lookup-string := "http://rs.tdwg.org/"||$vocab||"/doc/"||$local-id||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/"||$vocab||"/doc/"||$local-id||"/"||$date
      let $redirect-id := "/"||$vocab||"/doc/"||$local-id||"/"||$date
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handle ideosynchratic Darwin Core guides URI patterns of "/dwc/terms/guides/{doc}/" :)
declare
  %rest:path("/dwc/terms/guides/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-dwc-guides($acceptHeader,$local-id)
  {
  let $db := "docs"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($local-id,".")
      let $extension := substring-after($local-id,".")
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/guides/"||$stripped-local-name||"/"
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/guides/"||$local-id||"/"
      let $redirect-id := "/dwc/terms/guides/"||$local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handle ideosynchratic Darwin Core simple text version URI patterns of "/dwc/terms/simple/{versionDate}" (Darwin Core simple text versions) :)
declare
  %rest:path("/dwc/terms/simple/{$date}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-dwc-simple-versions($acceptHeader,$date)
  {
  let $db := "docs-versions"
  return
    if (contains($date,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($date,".")
      let $extension := substring-after($date,".")
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/simple/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/simple/"||$date
      let $redirect-id := "/dwc/terms/simple/"||$date
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handle ideosynchratic Darwin Core namespace version URI patterns of "/dwc/terms/namespace/{versionDate}" (Darwin Core namespace policy versions) :)
declare
  %rest:path("/dwc/terms/namespace/{$date}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-dwc-namespace-versions($acceptHeader,$date)
  {
  let $db := "docs-versions"
  return
    if (contains($date,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($date,".")
      let $extension := substring-after($date,".")
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/namespace/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/namespace/"||$date
      let $redirect-id := "/dwc/terms/namespace/"||$date
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(: Handle ideosynchratic Darwin Core guide version URI patterns of "/dwc/terms/guides/{docname}/{versionDate}" (Darwin Core standards documents versions) :)
declare
  %rest:path("/dwc/terms/guides/{$local-id}/{$date}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-dwc-guide-versions($acceptHeader,$local-id,$date)
  {
  let $db := "docs-versions"
  return
    if (contains($date,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($date,".")
      let $extension := substring-after($date,".")
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/guides/"||$local-id||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/dwc/terms/guides/"||$local-id||"/"||$date
      let $redirect-id := "/dwc/terms/guides/"||$local-id||"/"||$date
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(:----------------------------------------------------------------------------------------------:)
(: Vocabularies and term lists patterns :)

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
      return
      switch ($stripped-local-name)
        (: handle the special case of TDWG decisions :)
        case "decisions" return page:handle-repesentation($acceptHeader,$extension,"term-lists","http://rs.tdwg.org/decisions/")
        (: handle the special case of the dataset index :)
        case "index" return page:handle-repesentation($acceptHeader,$extension,"index","http://rs.tdwg.org/index")
        default return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/"||$local-id||"/"
      let $redirect-id := "/"||$local-id
      return
      switch ($local-id)
        (: handle the special case of TDWG decisions :)
        case "decisions" return page:see-also($acceptHeader,"/decisions","term-lists","http://rs.tdwg.org/decisions/")
        (: handle the special case of the simple Darwin Core guide :)
        case "index" return page:see-also($acceptHeader,"/index","index","http://rs.tdwg.org/index")
        default return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
 };

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

(: Handler for the special URI pattern for tdwgutility: term list versions under the "/dwc/terms/version/attributes/" subpath (TDGW utility term list versions) :)
declare
  %rest:path("/dwc/version/terms/attributes/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:content-negotiation-tdwgutility-term-list-versions($acceptHeader,$local-id)
  {
  let $db := "term-lists-versions"
  return
    if (contains($local-id,"."))
    then
      (: has an extension :)
      let $stripped-local-name := substring-before($local-id,".")
      let $extension := substring-after($local-id,".")
      let $lookup-string := "http://rs.tdwg.org/dwc/version/terms/attributes/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := "http://rs.tdwg.org/dwc/version/terms/attributes/"||$local-id
      let $redirect-id := $local-id
      return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

(:----------------------------------------------------------------------------------------------:)
(: Terms patterns :)

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

  let $result :=
    for $termlist in $termlistData
    where $termlist/list_localName/text() = $listLocalname
    return page:generic-simple-id($local-id,$termlist/database/text(),$acceptHeader)
  return
    if (count($result)=0)
    then page:not-found()
    else $result
  };


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

  let $result :=
    for $termlist in $termlistData
    where $termlist/list_localName/text() = $listLocalname
    return page:generic-simple-id($local-id,$termlist/database/text()||"-versions",$acceptHeader)
  return
    if (count($result)=0)
    then page:not-found()
    else $result
  };

(: Handler for the special URI pattern for tdwgutility: terms under the "/dwc/terms/attributes/" subpath (TDWG utility terms) :)
declare
  %rest:path("/dwc/terms/attributes/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:tdwgutility-terms($acceptHeader,$local-id)
  {
  page:generic-simple-id($local-id,"utility",$acceptHeader)
  };

(: Handler for the special URI pattern for tdwgutility: term versions under the "/dwc/terms/attributes/version/" subpath (TDGW utility term versions) :)
declare
  %rest:path("/dwc/terms/attributes/version/{$local-id}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:tdwgutility-term-versions($acceptHeader,$local-id)
  {
  page:generic-simple-id($local-id,"utility-versions",$acceptHeader)
  };

(: Patterns to handle all the inconsistent uses of the Darwin Core namespace :)
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
      return
      switch ($lookup-string)
        (: handle the special case of the tdwgutility: term list "/dwc/terms/attributes/". :)
        case "attributes" return page:handle-repesentation($acceptHeader,$extension,"term-lists","http://rs.tdwg.org/dwc/terms/attributes/")
        (: handle the special case of the simple Darwin Core guide :)
        case "simple" return page:handle-repesentation($acceptHeader,$extension,"docs","http://rs.tdwg.org/dwc/terms/simple/")
        (: handle the special case of the Darwin Core namespace policy :)
        case "namespace" return page:handle-repesentation($acceptHeader,$extension,"docs","http://rs.tdwg.org/dwc/terms/namespace/")
        (: handle the case of bookmarks to old quick reference guide :)
        (: Note: I used a 301 (moved permanently) redirect because we basically don't want this URL to be used any more :)
        case "index" return
                <rest:response>
                <http:response status="307">
                  <http:header name="location" value="https://dwc.tdwg.org/terms/"/>
                </http:response>
              </rest:response>
        default return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := $local-id
      let $redirect-id := $local-id
      return
      switch ($lookup-string)
        (: handle the special case of the tdwgutility: term list "/dwc/terms/attributes/". :)
        case "attributes" return page:see-also($acceptHeader,"/dwc/terms/attributes","term-lists","http://rs.tdwg.org/dwc/terms/attributes/")
        (: handle the special case of the simple Darwin Core guide :)
        case "simple" return page:see-also($acceptHeader,"/dwc/terms/simple","docs","http://rs.tdwg.org/dwc/terms/simple/")
       (: handle the special case of the Darwin Core namespace policy :)
        case "namespace" return page:see-also($acceptHeader,"/dwc/terms/namespace","docs","http://rs.tdwg.org/dwc/terms/namespace/")
        case "history" return
              (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
              (: This will redirect to the rs.tdwg.org repository readme :)
              <rest:response>
              <http:response status="307">
                <http:header name="location" value="https://github.com/tdwg/rs.tdwg.org/blob/master/README.md"/>
              </http:response>
            </rest:response>
        default return page:see-also($acceptHeader,$redirect-id,$db,$lookup-string)
  };

 (: Patterms to redirect legacy bookmarks :)
declare
  %rest:path("/dwc/terms/guides/{$local-id}/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-legacy-index-htm($acceptHeader,$local-id)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect to the "permanent URL", which then does a 302 to the Darwin Core website :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="{'/dwc/terms/guides/'||$local-id}"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/simple/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-legacy-simple-htm($acceptHeader)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect to the "permanent URL", which then does a 302 to the Darwin Core website :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="/dwc/terms/simple"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/namespace/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-legacy-namespace-htm($acceptHeader)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect to the "permanent URL", which then does a 302 to the Darwin Core website :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="/dwc/terms/namespace"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-legacy-dwc-landing-htm($acceptHeader)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect to the Darwin Core homepage :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="https://www.tdwg.org/standards/dwc/"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/index")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-index-legacy-dwc-landing-htm($acceptHeader)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect from http://rs.tdwg.org/dwc/index/ to the Darwin Core homepage :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="https://www.tdwg.org/standards/dwc/"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/history/decisions/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-legacy-decisions-index-htm($acceptHeader)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect to the TDWG Decisions page :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="/decisions"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/history/decisions")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-legacy-decisions-htm($acceptHeader)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect to the TDWG Decisions page :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="/decisions"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/history/versions/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-history-versions-index-htm($acceptHeader)
  {
    (: This is where the versions history has been redirecting to :)
    <rest:response>
    <http:response status="302">
      <http:header name="location" value="https://github.com/tdwg/dwc/blob/master/vocabulary/term_versions.csv"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/history/versions")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-history-versions-htm($acceptHeader)
  {
    (: This is where the versions history has been redirecting to :)
    <rest:response>
    <http:response status="302">
      <http:header name="location" value="https://github.com/tdwg/dwc/blob/master/vocabulary/term_versions.csv"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/history/dwctoabcd/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-dwctoabcd-versions-index-htm($acceptHeader)
  {
    (: This is where the versions history has been redirecting to :)
    <rest:response>
    <http:response status="302">
      <http:header name="location" value="https://github.com/tdwg/dwc/blob/master/vocabulary/term_versions.csv"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/history/dwctoabcd")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-dwctoabcd-versions-htm($acceptHeader)
  {
    (: This is where the versions history has been redirecting to :)
    <rest:response>
    <http:response status="302">
      <http:header name="location" value="https://github.com/tdwg/dwc/blob/master/vocabulary/term_versions.csv"/>
    </http:response>
  </rest:response>
  };

declare
  %rest:path("/dwc/terms/history/index.htm")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:dwc-legacy-history-index-htm($acceptHeader)
  {
    (: Note: I used a 301 (moved permanently) redirect because we basically don't want these URLs to be used any more :)
    (: This will redirect to the rs.tdwg.org repository readme :)
    <rest:response>
    <http:response status="307">
      <http:header name="location" value="https://github.com/tdwg/rs.tdwg.org/blob/master/README.md"/>
    </http:response>
  </rest:response>
  };



(:----------------------------------------------------------------------------------------------:)
(: Ideosyncratic redirects to fixed categories of resources :)
(: See documentation at http://docs.basex.org/wiki/RESTXQ#Forwards_and_Redirects :)
(: 302 redirects :)

(: Tapir redirects :)
declare %rest:path("/tapir/cns/{$path=.+}") function page:tapir-cns-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/tapir/cns/"||$path}</rest:redirect>};

declare %rest:path("/tapir/cs/{$path=.+}") function page:tapir-cs-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/tapir/cs/"||$path}</rest:redirect>};

(: This isn't working - gets a 404 
declare %rest:path("/tapir/1.0/schema/tdwg_tapir.xsd") function page:tapir10-schema-redirect()
 {<rest:redirect>{"https://raw.githubusercontent.com/tdwg/tapir/1.0/schema/tapir.xsd"}</rest:redirect>};
:)

declare %rest:path("/tapir/1.0/schema/tapir.xsd") function page:tapir10-tapir-redirect()
 {<rest:redirect>{"https://raw.githubusercontent.com/tdwg/tapir/master/schema/tapir.xsd"}</rest:redirect>};

(: This particular URL seems to be in use and redirects to this particular place :)
declare %rest:path("/tapir/1.0/schema/tdwg_tapir.xsd") function page:tapir10-tdwgtapir-redirect()
 {<rest:redirect>{"https://raw.githubusercontent.com/tdwg/infrastructure/master/rs.tdwg.org/tapir/1.0/schema/tapir.xsd"}</rest:redirect>};

(: TDWG ontology redirects :)
declare %rest:path("/ontology/{$path=.+}") function page:ontology-redirect($path)
{
    if (contains($path,"."))
    then
      <rest:redirect>{"http://tdwg.github.io/ontology/ontology/"||$path}</rest:redirect>
    else
      <rest:redirect>{"http://tdwg.github.io/ontology/ontology/"||$path||".rdf"}</rest:redirect>
};

declare %rest:path("/ontology2/{$path=.+}") function page:ontology2-redirect($path)
  {<rest:redirect>{"http://tdwg-ontology.googlecode.com/svn/trunk/ontology/"||$path}</rest:redirect>};

(: SDD redirects :)
declare %rest:path("/UBIF/{$path=.+}") function page:ubif-forward($path)
  {<rest:redirect>{"http://tdwg.github.io/sdd/"||$path}</rest:redirect>};

(:declare %rest:path("/sdd/{$path=.+}") function page:sdd-forward($path)
  {<rest:redirect>{"http://tdwg.github.io/sdd/"||$path}</rest:redirect>};:)

(: ABCD redirects. Currently they all have 303 redirects, so I've done that here as well. :)

(: ABCD2 terms :)
declare
  %rest:path("/abcd2/terms/{$path=[a-zA-Z0-9-._@]+}")
  function page:abcd2termsx-redirect($path)
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="{'https://abcd.tdwg.org/2.06/terms/#'||$path}" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd2/terms")
  function page:abcd2terms-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/2.06/terms/" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd2")
  function page:abcd2-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/xml/documentation/primer/2.06/" />
    </http:response>
  </rest:response>
};

(: ABCD EFG terms :)

declare
  %rest:path("/abcd-efg/terms/{$path=[a-zA-Z0-9-._@]+}")
  function page:abcdefgtermsx-redirect($path)
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="{'http://terms.tdwg.org/wiki/abcd-efg:'||$path}" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd-efg/terms")
  function page:abcdefgterms-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="http://terms.tdwg.org/wiki/ABCD_EFG" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd-efg")
  function page:abcdefg-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="http://terms.tdwg.org/wiki/ABCD_EFG" />
    </http:response>
  </rest:response>
};

(: ABCD 3.0 terms :)

declare
  %rest:path("/abcd")
  function page:abcd-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/" />
    </http:response>
  </rest:response>
};

(: core ontology :)

declare
  %rest:path("/abcd/terms/{$path=[a-zA-Z0-9-._@]+}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:abcdtermsx-redirect($path, $acceptHeader)
  {
    let $header := page:extract-html-header($acceptHeader)
    return switch ($header)
      case "application/rdf+xml" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_concepts.owl" />
            </http:response>
         </rest:response>

      case "text/turtle" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_concepts.ttl" />
            </http:response>
         </rest:response>

      case "application/ld+json" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_concepts.jsonld" />
            </http:response>
         </rest:response>

      case "text/html" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="{'https://abcd.tdwg.org/terms/#'||$path}" />
            </http:response>
         </rest:response>

      default return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_concepts.owl" />
            </http:response>
         </rest:response>
};

(: mappings ontology :)

declare
  %rest:path("/abcd/mappings/{$path=[a-zA-Z0-9-._@]+}")
  %rest:header-param("Accept","{$acceptHeader}")
  function page:abcdmappingsx-redirect($path, $acceptHeader)
  {
    let $header := page:extract-html-header($acceptHeader)
    return switch ($header)
      case "application/rdf+xml" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_mappings.owl" />
            </http:response>
         </rest:response>

      case "text/turtle" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_mappings.ttl" />
            </http:response>
         </rest:response>

      case "application/ld+json" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_mappings.jsonld" />
            </http:response>
         </rest:response>

      case "text/html" return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="{'https://abcd.tdwg.org/mappings/#'||$path}" />
            </http:response>
         </rest:response>

      default return 
         <rest:response>
            <http:response status="303">
              <http:header name="location" value="https://abcd.tdwg.org/ontology/abcd_mappings.owl" />
            </http:response>
         </rest:response>
};

(: ABCD history URLs :)
declare
  %rest:path("/abcd/terms/history/{$path=[a-zA-Z0-9-._@]+}")
  function page:history-redirect($path)
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="{'https://abcd.tdwg.org/terms/history/#'||$path}" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/terms/?")
  function page:termsq-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/terms/" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/mapping/?")
  function page:mappingq-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/terms/mappings/" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/?")
  function page:abcdq-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/" />
    </http:response>
  </rest:response>
};

(: ABCD legacy URLs :)
declare
  %rest:path("/abcd/2.06/{$path=[a-zA-Z0-9-._@]+}")
  function page:abcd206x-redirect($path)
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="{'https://abcd.tdwg.org/legacy/2.06/'||$path}" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/2.06")
  function page:abcd206-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/legacy/2.06/" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/1.2/{$path=[a-zA-Z0-9-._@]+}")
  function page:abcd12x-redirect($path)
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="{'https://abcd.tdwg.org/legacy/1.2/'||$path}" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/2.06/a/ABCD_2.06a.xsd")
  function page:abcd206a-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/legacy/2.06/a/ABCD_2.06a.xsd" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/2.06/b/ABCD_2.06b.xsd")
  function page:abcd206b-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/legacy/2.06/b/ABCD_2.06b.xsd" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/1.2")
  function page:abcd12-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/legacy/1.2/" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/ABCD_/{$path=[a-zA-Z0-9-._@]+}")
  function page:abcdABCD_x-redirect($path)
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="{'https://abcd.tdwg.org/legacy/'||$path}" />
    </http:response>
  </rest:response>
};

declare
  %rest:path("/abcd/ABCD_")
  function page:abcdABCD_-redirect()
  {
   <rest:response>
    <http:response status="303">
      <http:header name="location" value="https://abcd.tdwg.org/legacy/ABCD_/" />
    </http:response>
  </rest:response>
};

(: Darwin Core generic redirects when specific content negotiation doesn't kick in :)
(: must have subpath to not override the vocabulary terms :)
declare %rest:path("/dwc/xsd/{$path=.+}") function page:dwc-xsd-redirect($path)
 {<rest:redirect>{"https://dwc.tdwg.org/xml/"||$path}</rest:redirect>};

declare %rest:path("/dwc/text/{$path=.+}") function page:dwc-text-redirect($path)
 {<rest:redirect>{"https://dwc.tdwg.org/text/"||$path}</rest:redirect>};

declare %rest:path("/dwc/rdf/{$path=.+}") function page:dwc-rdf-redirect($path)
 {<rest:redirect>{"https://dwc.tdwg.org/rdf/"||$path}</rest:redirect>};

declare %rest:path("/dwc/downloads/{$path=.+}") function page:dwc-downloads-redirect($path)
 {<rest:redirect>{"https://dwc.tdwg.org/downloads/"||$path}</rest:redirect>};

declare %rest:path("/dwc/examples/{$path=.+}") function page:dwc-examples-redirect($path)
 {<rest:redirect>{"https://dwc.tdwg.org/examples/"||$path}</rest:redirect>};

(: defunct styling
declare %rest:path("/dwc/DarwinCore_files/{$path=.+}") function page:dwc-files-redirect($path)
 {<rest:redirect>{"https://tdwg.github.io/dwc/DarwinCore_files/"||$path}</rest:redirect>};
:)

declare %rest:path("/dwc/index_legacy_rddl.html") function page:tdwg-legacy-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/index_legacy_rddl.html"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_basetypes.xsd") function page:tdwg-basetypes-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_basetypes.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_core.xsd") function page:tdwg-dw-core-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_dw_core.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_curatorial.xsd") function page:tdwg-dw-curat-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_dw_curatorial.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_element.xsd") function page:tdwg-dw-element-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_dw_element.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_geospatial.xsd") function page:tdwg-dw-geo-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_dw_geospatial.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_record.xsd") function page:tdwg-dw-record-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_dw_record.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_dw_record_tapir.xsd") function page:tdwg-dw-tapir-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_dw_record_tapir.xsd"}</rest:redirect>};

declare %rest:path("/dwc/tdwg_gml.xsd") function page:tdwg-gml-redirect()
 {<rest:redirect>{"https://dwc.tdwg.org/tdwg_gml.xsd"}</rest:redirect>};


(:----------------------------------------------------------------------------------------------:)
(: Second-level functions :)

(: Generic 404 error message for errors :)
declare
  %rest:error("*")
function page:user-error() {
page:not-found()
};

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
  if (page:find-db($lookup-string,$db))  (: check whether the resource is in the database :)
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
  then 
    switch ($db)
      case "docs" return page:handle-docs-html($lookup-string)
      case "docs-versions" return page:handle-docs-versions-html($lookup-string)
      case "index" return page:temp-redirect("https://tdwg.github.io/rs.tdwg.org/","")
      default return page:handle-html($db,$lookup-string)
  else
  (: I moved this within the ELSE statement because it interferes with the HTML redirect if I leave it before the IF :)
  <rest:response>
    <output:serialization-parameters>
      <output:media-type value='{$response-media-type}'/>
    </output:serialization-parameters>
  </rest:response>,
  page:main-db($lookup-string,$flag,"single",$db)
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
      case "decisions" return (page:success(),html:generate-decisions-html($lookup-string))
      default return page:not-found()
  else
    (: this sort of redirect only makes sense for terms and term versions :)
    let $base :=
      if ($redirectItem/useNamespace/text()="yes")
      then $redirectItem/prefix/text()||$redirectItem/namespace/text()||$redirectItem/connector/text()
      else $redirectItem/prefix/text()
    return page:temp-redirect($base,$lookup-string)
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

(: Function to redirect to a web page for standards documents versions :)
declare function page:handle-docs-versions-html($lookup-string)
{
let $redirectFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/docs-versions/docs-versions.csv"
let $redirectDoc := http:send-request(<http:request method='get' href='{$redirectFilePath}'/>)[2]
let $redirectDataRaw := csv:parse($redirectDoc, map { 'header' : true(),'separator' : "," })
let $redirectData := $redirectDataRaw/csv/record
for $redirectItem in $redirectData
where $redirectItem/version_iri/text() = $lookup-string
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
  if(page:find-db($lookup-string,$db))  (: check whether the resource is in the database :)
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
(: Utility functions to set media type-dependent values, etc. :)

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


(: Code from https://raw.githubusercontent.com/baskaufs/guid-o-matic/master/serialize.xqm :)
(: part of Guid-O-Matic 2.0 https://github.com/baskaufs/guid-o-matic . You are welcome to reuse or hack in any way :)

(: These two functions copied from FunctX http://www.xqueryfunctions.com/ :)

declare function page:substring-after-last
  ( $arg as xs:string? ,
    $delim as xs:string )  as xs:string {

   replace ($arg,concat('^.*',page:escape-for-regex($delim)),'')
 } ;
 
 declare function page:escape-for-regex
  ( $arg as xs:string? )  as xs:string {

   replace($arg,
           '(\.|\[|\]|\\|\||\-|\^|\$|\?|\*|\+|\{|\}|\(|\))','\\$1')
 } ;
(:--------------------------------------------------------------------------------------------------:)

declare function page:main-db($id,$serialization,$singleOrDump,$db)
{
(: This database version is intended to be used with the restxq-db web service.  So output to a file is always
disabled.  Instead of using the last parameter to pass the save file path, in this function, it's used to specify
the database to be used in the function call. :)
(: let $db := "tang-song" :)
let $outputToFile := "false"

let $constants := fn:collection($db)//constants/record
let $domainRoot := $constants//domainRoot/text()
let $outputDirectory := $constants//outputDirectory/text()
let $baseIriColumn := $constants//baseIriColumn/text()
let $modifiedColumn := $constants//modifiedColumn/text()
let $outFileNameAfter := $constants//outFileNameAfter/text()

let $columnInfo := fn:collection($db)//column-index/record
let $namespaces := fn:collection($db)//namespaces/record
let $classes := fn:collection($db)//base-classes/record
let $linkedClasses := fn:collection($db)//linked-classes/record
let $metadata := fn:collection($db)/metadata/record
let $linkedMetadata := fn:collection($db)//linked-metadata/file
  
(: The main function returns a single string formed by concatenating all of the assembled pieces of the document :)
return 
  if ($outputToFile="true")
  then
    (: Creates the output directory specified in the constants.csv file if it doesn't already exist.  Then writes into a file having the name passed via the $id parameter concatenated with an appropriate file extension. uses default UTF-8 encoding :)
    (file:create-dir($outputDirectory),
    
    (: If the $id is a full IRI or long string, use only the part after the delimiter in $outFileNameAfter as the file name.  Otherwise, use the entire value of $id as the file name:) 
    if ($outFileNameAfter) 
    then file:write-text($outputDirectory||page:substring-after-last($id, $outFileNameAfter)||page:extension($serialization),page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn))
    else file:write-text($outputDirectory||$id||page:extension($serialization),page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn))
    ,
    
    (: put this in the Result window so that the user can tell that something happened :)
    "Completed file write of "||$id||page:extension($serialization)||" at "||fn:current-dateTime()
    )
  else
    (: simply output the string to the Result window :)
    page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn)
};
(:--------------------------------------------------------------------------------------------------:)

declare function page:main($id,$serialization,$repoPath,$pcRepoLocation,$singleOrDump,$outputToFile)
{

(: This is an attempt to allow the necessary CSV files to load on any platform without hard-coding any paths here.  I know it works for PCs, but am not sure how consistently it works on non-PCs :)
let $localFilesFolderUnix := 
(:  if (fn:substring(file:current-dir(),1,2) = "C:") 
  then :)
    (: the computer is a PC with a C: drive, the path specified in the function arguments are substituted :)
    "file:///"||$pcRepoLocation||$repoPath
(:  else
     it's a Mac with the query running from a repo located at the default under the user directory
    file:current-dir() || "/Repositories/"||$repoPath :)

let $constantsDoc := file:read-text(concat($localFilesFolderUnix, 'constants.csv'))
let $xmlConstants := csv:parse($constantsDoc, map { 'header' : true(),'separator' : "," })
let $constants := $xmlConstants/csv/record

let $domainRoot := $constants//domainRoot/text()
let $coreDoc := $constants//coreClassFile/text()
let $coreClassPrefix := substring-before($coreDoc,".")
let $outputDirectory := $constants//outputDirectory/text()
let $metadataSeparator := $constants//separator/text()
let $baseIriColumn := $constants//baseIriColumn/text()
let $modifiedColumn := $constants//modifiedColumn/text()
let $outFileNameAfter := $constants//outFileNameAfter/text()

let $columnIndexDoc := file:read-text($localFilesFolderUnix||$coreClassPrefix||'-column-mappings.csv')
let $xmlColumnIndex := csv:parse($columnIndexDoc, map { 'header' : true(),'separator' : "," })
let $columnInfo := $xmlColumnIndex/csv/record

let $namespaceDoc := file:read-text(concat($localFilesFolderUnix,'namespace.csv'))
let $xmlNamespace := csv:parse($namespaceDoc, map { 'header' : true(),'separator' : "," })
let $namespaces := $xmlNamespace/csv/record

let $classesDoc := file:read-text($localFilesFolderUnix||$coreClassPrefix||'-classes.csv')
let $xmlClasses := csv:parse($classesDoc, map { 'header' : true(),'separator' : "," })
let $classes := $xmlClasses/csv/record

let $linkedClassesDoc := file:read-text(concat($localFilesFolderUnix,'linked-classes.csv'))
let $xmlLinkedClasses := csv:parse($linkedClassesDoc, map { 'header' : true(),'separator' : "," })
let $linkedClasses := $xmlLinkedClasses/csv/record

let $metadataDoc := file:read-text($localFilesFolderUnix ||$coreDoc)
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

let $linkedMetadata :=
      for $class in $linkedClasses
      let $linkedDoc := $class/filename/text()
      let $linkedClassPrefix := substring-before($linkedDoc,".")

      let $classMappingDoc := file:read-text(concat($localFilesFolderUnix,$linkedClassPrefix,"-column-mappings.csv"))
      let $xmlClassMapping := csv:parse($classMappingDoc, map { 'header' : true(),'separator' : "," })
      let $classClassesDoc := file:read-text(concat($localFilesFolderUnix,$linkedClassPrefix,"-classes.csv"))
      let $xmlClassClasses := csv:parse($classClassesDoc, map { 'header' : true(),'separator' : "," })
      let $classMetadataDoc := file:read-text(concat($localFilesFolderUnix,$linkedDoc))
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
  
(: The main function returns a single string formed by concatenating all of the assembled pieces of the document :)
return 
  if ($outputToFile="true")
  then
    (: Creates the output directory specified in the constants.csv file if it doesn't already exist.  Then writes into a file having the name passed via the $id parameter concatenated with an appropriate file extension. uses default UTF-8 encoding :)
    (file:create-dir($outputDirectory),
    
    (: If the $id is a full IRI or long string, use only the part after the delimiter in $outFileNameAfter as the file name.  Otherwise, use the entire value of $id as the file name:) 
    if ($outFileNameAfter) 
    then file:write-text($outputDirectory||page:substring-after-last($id, $outFileNameAfter)||page:extension($serialization),page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn))
    else file:write-text($outputDirectory||$id||page:extension($serialization),page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn))
    ,
    
    (: put this in the Result window so that the user can tell that something happened :)
    "Completed file write of "||$id||page:extension($serialization)||" at "||fn:current-dateTime()
    )
  else
    (: simply output the string to the Result window :)
    page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn)
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:main-github($id,$serialization,$baseURI,$repoName,$singleOrDump,$outputToFile)
{
    
(: Despite the variable name, this is hacked to be the HTTP URI of the github repo online. :)
let $localFilesFolderUnix := concat($baseURI,$repoName,"/")

let $constantsDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||'constants.csv'}'/>)[2]
let $xmlConstants := csv:parse($constantsDoc, map { 'header' : true(),'separator' : "," })
let $constants := $xmlConstants/csv/record

let $domainRoot := $constants//domainRoot/text()
let $coreDoc := $constants//coreClassFile/text()
let $coreClassPrefix := substring-before($coreDoc,".")
let $outputDirectory := $constants//outputDirectory/text()
let $metadataSeparator := $constants//separator/text()
let $baseIriColumn := $constants//baseIriColumn/text()
let $modifiedColumn := $constants//modifiedColumn/text()
let $outFileNameAfter := $constants//outFileNameAfter/text()

let $columnIndexDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$coreClassPrefix||'-column-mappings.csv'}'/>)[2]
let $xmlColumnIndex := csv:parse($columnIndexDoc, map { 'header' : true(),'separator' : "," })
let $columnInfo := $xmlColumnIndex/csv/record

let $namespaceDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||'namespace.csv'}'/>)[2]
let $xmlNamespace := csv:parse($namespaceDoc, map { 'header' : true(),'separator' : "," })
let $namespaces := $xmlNamespace/csv/record

let $classesDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$coreClassPrefix||'-classes.csv'}'/>)[2]
let $xmlClasses := csv:parse($classesDoc, map { 'header' : true(),'separator' : "," })
let $classes := $xmlClasses/csv/record

let $linkedClassesDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||'linked-classes.csv'}'/>)[2]
let $xmlLinkedClasses := csv:parse($linkedClassesDoc, map { 'header' : true(),'separator' : "," })
let $linkedClasses := $xmlLinkedClasses/csv/record

let $metadataDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix ||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

let $linkedMetadata :=
      for $class in $linkedClasses
      let $linkedDoc := $class/filename/text()
      let $linkedClassPrefix := substring-before($linkedDoc,".")

      let $classMappingDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$linkedClassPrefix||"-column-mappings.csv"}'/>)[2]
      let $xmlClassMapping := csv:parse($classMappingDoc, map { 'header' : true(),'separator' : "," })
      let $classClassesDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$linkedClassPrefix||"-classes.csv"}'/>)[2]
      let $xmlClassClasses := csv:parse($classClassesDoc, map { 'header' : true(),'separator' : "," })
      let $classMetadataDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$linkedDoc}'/>)[2]
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
  
(: The main function returns a single string formed by concatenating all of the assembled pieces of the document :)
return 
  if ($outputToFile="true")
  then
    (: Creates the output directory specified in the constants.csv file if it doesn't already exist.  Then writes into a file having the name passed via the $id parameter concatenated with an appropriate file extension. uses default UTF-8 encoding :)
    (file:create-dir($outputDirectory),
    
    (: If the $id is a full IRI or long string, use only the part after the delimiter in $outFileNameAfter as the file name.  Otherwise, use the entire value of $id as the file name:) 
    if ($outFileNameAfter) 
    then file:write-text($outputDirectory||page:substring-after-last($id, $outFileNameAfter)||page:extension($serialization),page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn))
    else file:write-text($outputDirectory||$id||page:extension($serialization),page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn))
    ,
    
    (: put this in the Result window so that the user can tell that something happened :)
    "Completed file write of "||$id||page:extension($serialization)||" at "||fn:current-dateTime()
    )
  else
    (: simply output the string to the Result window :)
    page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn)
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:find($id,$repoPath,$pcRepoLocation)
{

(: This is an attempt to allow the necessary CSV files to load on any platform without hard-coding any paths here.  I know it works for PCs, but am not sure how consistently it works on non-PCs :)
let $localFilesFolderUnix := 
(:  if (fn:substring(file:current-dir(),1,2) = "C:") 
  then :)
    (: the computer is a PC with a C: drive, the path specified in the function arguments are substituted :)
    "file:///"||$pcRepoLocation||$repoPath
(:  else
     it's a Mac with the query running from a repo located at the default under the user directory
    file:current-dir() || "/Repositories/"||$repoPath :)

let $constantsDoc := file:read-text(concat($localFilesFolderUnix, 'constants.csv'))
let $xmlConstants := csv:parse($constantsDoc, map { 'header' : true(),'separator' : "," })
let $constants := $xmlConstants/csv/record

let $domainRoot := $constants//domainRoot/text()
let $coreDoc := $constants//coreClassFile/text()
let $coreClassPrefix := substring-before($coreDoc,".")
let $outputDirectory := $constants//outputDirectory/text()
let $metadataSeparator := $constants//separator/text()
let $baseIriColumn := $constants//baseIriColumn/text()
let $modifiedColumn := $constants//modifiedColumn/text()
let $outFileNameAfter := $constants//outFileNameAfter/text()

let $columnIndexDoc := file:read-text($localFilesFolderUnix||$coreClassPrefix||'-column-mappings.csv')
let $xmlColumnIndex := csv:parse($columnIndexDoc, map { 'header' : true(),'separator' : "," })
let $columnInfo := $xmlColumnIndex/csv/record

let $namespaceDoc := file:read-text(concat($localFilesFolderUnix,'namespace.csv'))
let $xmlNamespace := csv:parse($namespaceDoc, map { 'header' : true(),'separator' : "," })
let $namespaces := $xmlNamespace/csv/record

let $classesDoc := file:read-text($localFilesFolderUnix||$coreClassPrefix||'-classes.csv')
let $xmlClasses := csv:parse($classesDoc, map { 'header' : true(),'separator' : "," })
let $classes := $xmlClasses/csv/record

let $linkedClassesDoc := file:read-text(concat($localFilesFolderUnix,'linked-classes.csv'))
let $xmlLinkedClasses := csv:parse($linkedClassesDoc, map { 'header' : true(),'separator' : "," })
let $linkedClasses := $xmlLinkedClasses/csv/record

let $metadataDoc := file:read-text($localFilesFolderUnix ||$coreDoc)
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

let $linkedMetadata :=
      for $class in $linkedClasses
      let $linkedDoc := $class/filename/text()
      let $linkedClassPrefix := substring-before($linkedDoc,".")

      let $classMappingDoc := file:read-text(concat($localFilesFolderUnix,$linkedClassPrefix,"-column-mappings.csv"))
      let $xmlClassMapping := csv:parse($classMappingDoc, map { 'header' : true(),'separator' : "," })
      let $classClassesDoc := file:read-text(concat($localFilesFolderUnix,$linkedClassPrefix,"-classes.csv"))
      let $xmlClassClasses := csv:parse($classClassesDoc, map { 'header' : true(),'separator' : "," })
      let $classMetadataDoc := file:read-text(concat($localFilesFolderUnix,$linkedDoc))
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
  
return 
      (: each record in the database must be checked for a match to the requested URI :)
      for $record in $metadata
      where $record/*[local-name()=$baseIriColumn]/text()=$id
      return true()      
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:find-db($id,$db)
{
(: let $db := "tang-song" :)

let $constants := fn:collection($db)//constants/record
let $baseIriColumn := $constants//baseIriColumn/text()

let $metadata := fn:collection($db)/metadata/record
  
return 
      (: each record in the database must be checked for a match to the requested URI :)
      for $record in $metadata
      where $record/*[local-name()=$baseIriColumn]/text()=$id
      return true()      
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:find-github($id,$baseURI,$repoName)
{

(: Despite the variable name, this is hacked to be the HTTP URI of the github repo online. :)
let $localFilesFolderUnix := concat($baseURI,$repoName,"/")

let $constantsDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||'constants.csv'}'/>)[2]
let $xmlConstants := csv:parse($constantsDoc, map { 'header' : true(),'separator' : "," })
let $constants := $xmlConstants/csv/record

let $domainRoot := $constants//domainRoot/text()
let $coreDoc := $constants//coreClassFile/text()
let $coreClassPrefix := substring-before($coreDoc,".")
let $outputDirectory := $constants//outputDirectory/text()
let $metadataSeparator := $constants//separator/text()
let $baseIriColumn := $constants//baseIriColumn/text()
let $modifiedColumn := $constants//modifiedColumn/text()
let $outFileNameAfter := $constants//outFileNameAfter/text()

let $columnIndexDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$coreClassPrefix||'-column-mappings.csv'}'/>)[2]
let $xmlColumnIndex := csv:parse($columnIndexDoc, map { 'header' : true(),'separator' : "," })
let $columnInfo := $xmlColumnIndex/csv/record

let $namespaceDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||'namespace.csv'}'/>)[2]
let $xmlNamespace := csv:parse($namespaceDoc, map { 'header' : true(),'separator' : "," })
let $namespaces := $xmlNamespace/csv/record

let $classesDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$coreClassPrefix||'-classes.csv'}'/>)[2]
let $xmlClasses := csv:parse($classesDoc, map { 'header' : true(),'separator' : "," })
let $classes := $xmlClasses/csv/record

let $linkedClassesDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||'linked-classes.csv'}'/>)[2]
let $xmlLinkedClasses := csv:parse($linkedClassesDoc, map { 'header' : true(),'separator' : "," })
let $linkedClasses := $xmlLinkedClasses/csv/record

let $metadataDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix ||$coreDoc}'/>)[2]
let $xmlMetadata := csv:parse($metadataDoc, map { 'header' : true(),'separator' : $metadataSeparator })
let $metadata := $xmlMetadata/csv/record

let $linkedMetadata :=
      for $class in $linkedClasses
      let $linkedDoc := $class/filename/text()
      let $linkedClassPrefix := substring-before($linkedDoc,".")

      let $classMappingDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix,$linkedClassPrefix||"-column-mappings.csv"}'/>)[2]
      let $xmlClassMapping := csv:parse($classMappingDoc, map { 'header' : true(),'separator' : "," })
      let $classClassesDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix||$coreClassPrefix||'-classes.csv'}'/>)[2]
      let $xmlClassClasses := csv:parse($classClassesDoc, map { 'header' : true(),'separator' : "," })
      let $classMetadataDoc := http:send-request(<http:request method='get' href='{$localFilesFolderUnix,$linkedDoc}'/>)[2]
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
  
return
      (: each record in the database must be checked for a match to the requested URI :)
      for $record in $metadata
      where $record/*[local-name()=$baseIriColumn]/text()=$id
      return true()
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:generate-entire-document($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn)
{
concat( 
  (: the namespace abbreviations only needs to be generated once for the entire document :)
  page:list-namespaces($namespaces,$serialization),
  if($serialization = 'json')
  then
    (: When each each resource description in each record is generated as json, it has a trailing comma.  The last one must be removed before closing the container for the array and document :)
    page:remove-last-comma(page:generate-records($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn))
  else 
    page:generate-records($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn)
  ,
  page:close-container($serialization) 
  ) 
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:generate-records($id,$linkedMetadata,$metadata,$domainRoot,$classes,$columnInfo,$serialization,$namespaces,$constants,$singleOrDump,$baseIriColumn,$modifiedColumn)
{
string-join( 
  if ($singleOrDump = "dump")
  then
    (: this case outputs every record in the database :)
    for $record in $metadata
    let $baseIRI := $domainRoot||$record/*[local-name()=$baseIriColumn]/text()
    let $modified := $record/*[local-name()=$modifiedColumn]/text()
    return page:generate-a-record($record,$linkedMetadata,$baseIRI,$domainRoot,$modified,$classes,$columnInfo,$serialization,$namespaces,$constants)
  else
    (: for a single record, each record in the database must be checked for a match to the requested URI :)
    for $record in $metadata
    where $record/*[local-name()=$baseIriColumn]/text()=$id
    let $baseIRI := $domainRoot||$record/*[local-name()=$baseIriColumn]/text()
    let $modified := $record/*[local-name()=$modifiedColumn]/text()
    return page:generate-a-record($record,$linkedMetadata,$baseIRI,$domainRoot,$modified,$classes,$columnInfo,$serialization,$namespaces,$constants)
  )  
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:generate-a-record($record,$linkedMetadata,$baseIRI,$domainRoot,$modified,$classes,$columnInfo,$serialization,$namespaces,$constants)
{
        
          (: Generate unabbreviated URIs and blank node identifiers. This must be done for every record separately since the UUIDs generated for the blank node identifiers must be the same within a record, but differ among records. :)
          
          let $IRIs := page:construct-iri($baseIRI,$classes) 
          (: generate a description for each class of resource included in the record :)
          for $modifiedClass in $IRIs
          return page:describe-resource($IRIs,$columnInfo,$record,$modifiedClass,$serialization,$namespaces,"") 
          ,
          
          (: now step through each class that's linked to the root class by many-to-one relationships and generate the resource description for each linked resource in that class :)
          for $linkedClass in $linkedMetadata
          return (
            (: determine the constants for the linked class :)
            let $linkColumn := $linkedClass/link_column/text()
            let $linkProperty := $linkedClass/link_property/text()
            let $suffix1 := $linkedClass/suffix1/text()
            let $linkCharacters := $linkedClass/link_characters/text()
            let $suffix2 := $linkedClass/suffix2/text()
            let $forwardLink :=
                  if ( exists($linkedClass/forward_link/text()) )
                  then $linkedClass/forward_link/text()
                  else "null"
            
            for $linkedClassRecord in $linkedClass/metadata/record
            where $baseIRI=$domainRoot||$linkedClassRecord/*[local-name()=$linkColumn]/text()
            
            (: generate an IRI or bnode for the instance of the linked class based on the convention for that class. 
            If the value of $linkCharacters is "http", then use the value in the $suffix1 column as the URI of the linked class instance :)
            let $linkedClassIRI := 
                    if (fn:substring($suffix1,1,2)="_:")
                    then
                        concat("_:",random:uuid() )
                    else
                            if ($linkCharacters="http")
                            then
                                $linkedClassRecord/*[local-name()=$suffix1]/text()
                            else
                            $baseIRI||"#"||$linkedClassRecord/*[local-name()=$suffix1]/text()||$linkCharacters||$linkedClassRecord/*[local-name()=$suffix2]/text()
            return (
                    (: Construct the descriptions of the linked class instances :)
                    let $linkedIRIs := page:construct-iri($linkedClassIRI,$linkedClass/classes/record)
                    let $extraTriple := if ($linkProperty = "null")
                                        then ""
                                        else
                                            (: The $extraTriple makes the backlink from the linked resource to the root class :)
                                            page:iri($linkProperty,$baseIRI,$serialization,$namespaces)
                    for $linkedModifiedClass in $linkedIRIs
                    return
                       page:describe-resource($linkedIRIs,$linkedClass/mapping/record,$linkedClassRecord,$linkedModifiedClass,$serialization,$namespaces,$extraTriple)
                    ,
                    (: This provides an option to create a forward link from the root class resource to the linked resource:)
                    if ($forwardLink = "null")
                    then ()
                    else
                      (: construct a single triple :)
                      concat(
                            (: the last-item function removes trailing delimiters if necessary for a serialization :)
                            page:last-item(concat(
                                  page:subject($baseIRI,$serialization),
                                  page:iri($forwardLink,$linkedClassIRI,$serialization,$namespaces)
                                  )
                                  , $serialization),
                            (: The page:type function with "null" type simply closes the container appropriately for the serialization. :)
                            page:type("null",$serialization,$namespaces),
                            (: each described resource must be separated by a comma in JSON. If a resource is the last described in the the array, the trailing comma will be removed after they are all concatenated. :)
                            if ($serialization="json")
                            then ",&#10;"
                            else ""
                            )
                    )
            )
            ,
            
            (: The document description is done once for each record. Suppress if the document class has a value of "null" :)
            if ($constants//documentClass/text() = "null")
            then
              ()
            else
              page:describe-document($baseIRI,$modified,$serialization,$namespaces,$constants)
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:describe-document($baseIRI,$modified,$serialization,$namespaces,$constants)
{
  let $type := $constants//documentClass/text()
  let $suffix := page:extension($serialization)
  (: If the URI ends in a slash, e.g. http://example.org/ex/, then remove the trailing slash before appending the suffix. :)
  (: I.e. http://example.org/ex.ttl, not http://example.org/ex/.ttl :)
  let $iri := concat(page:remove-trailing-slash($baseIRI),$suffix)
  return concat(
    page:subject($iri,$serialization),
    page:plain-literal("dc:format",page:media-type($serialization),$serialization),
    page:plain-literal("dc:creator",$constants//creator/text(),$serialization),
    
    page:iri("dcterms:references",$baseIRI,$serialization,$namespaces),
    if ($modified)
    then page:datatyped-literal("dcterms:modified",$modified,"xsd:dateTime",$serialization,$namespaces)
    else "",
    page:type($type,$serialization,$namespaces),
    
    (: each described resource must be separated by a comma in JSON. The final trailing comma for all resources will be removed after they are all concatenated. :)
    if ($serialization="json")
    then ",&#10;"
    else ""

  )  
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:remove-trailing-slash($temp)
{
  if (fn:ends-with($temp, '/'))
  then
    fn:substring($temp,1,fn:string-length($temp)-1)
  else
    $temp
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:remove-last-comma($temp)
{
  concat(fn:substring($temp,1,fn:string-length($temp)-2),"&#10;")
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:replace-semicolon-with-period($temp)
{
  concat(fn:substring($temp,1,fn:string-length($temp)-2),".&#10;")
};

(:--------------------------------------------------------------------------------------------------:)

(: if the last item in a property-value list is not followed by a type declaration, a trailing delimiter may need removal :)
declare function page:last-item($propertyBlock, $serialization)
{
if ($serialization = 'json')
then 
  (: For JSON, only the trailing comma needs to be removed. :)
  page:remove-last-comma($propertyBlock)
else 
    if ($serialization = 'turtle')
    then
        (: for Turtle, the trailing semicolon must be replaced with a final period :) 
        page:replace-semicolon-with-period($propertyBlock)
    else
        (: for XML there are no trailing delimiters, so nothing to remove. :)
        $propertyBlock
};

(:--------------------------------------------------------------------------------------------------:)

(: This generates the list of namespace abbreviations used :)
declare function page:list-namespaces($namespaces,$serialization)
{  
(: Because this is the beginning of the file, it also opens the root container for the serialization (if any) :)
switch ($serialization)
    case "turtle" return concat(
                          string-join(page:curie-value-pairs($namespaces,$serialization)),
                          "&#10;"
                        )
    case "xml" return concat(
                          "<rdf:RDF&#10;",
                          string-join(page:curie-value-pairs($namespaces,$serialization)),
                          ">&#10;"
                        )
    case "json" return concat(
                          "{&#10;",
                          '"@context": {&#10;',
                          page:remove-last-comma(string-join(page:curie-value-pairs($namespaces,$serialization))),
                          '},&#10;',
                          '"@graph": [&#10;'
                        )
    default return ""
};

(:--------------------------------------------------------------------------------------------------:)

(: generate sequence of CURIE,value pairs :)
declare function page:curie-value-pairs($namespaces,$serialization)
{
  for $namespace in $namespaces
  return switch ($serialization)
        case "turtle" return concat("@prefix ",$namespace/curie/text(),": <",$namespace/value/text(),">.&#10;")
        case "xml" return concat('xmlns:',$namespace/curie/text(),'="',$namespace/value/text(),'"&#10;')
        case "json" return concat('"',$namespace/curie/text(),'": "',$namespace/value/text(),'",&#10;')
        default return ""
};

(:--------------------------------------------------------------------------------------------------:)

(: This function describes a single instance of the type of resource being described by the table :)
declare function page:describe-resource($IRIs,$columnInfo,$record,$class,$serialization,$namespaces,$extraTriple)
{  
(: Note: the page:subject function sets up any string necessary to open the container, and the page:type function closes the container :)
let $type := $class/class/text()
let $id := $class/id/text()
let $iri := $class/fullId/text()
let $propertyBlock := 
  concat(
    page:subject($iri,$serialization),
    string-join(page:property-value-pairs($IRIs,$columnInfo,$record,$id,$serialization,$namespaces)),
    
    (: make the backlink only for the instance of the primary class in a table :)
    if ($id="$root")
    then $extraTriple
    else ""
  )
return (
  if ($type = 'null')
  then
    (: if the type declaration is omitted, then delimiters may need to be removed from the last property/value pair :)
    page:last-item($propertyBlock, $serialization)
  else
    (: if there is a type declaration, no action needed on removing delimiters :)
    $propertyBlock
  ,
  page:type($type,$serialization,$namespaces),
  (: each described resource must be separated by a comma in JSON. If a resource is the last described in the the array, the trailing comma will be removed after they are all concatenated. :)
  if ($serialization="json")
  then ",&#10;"
  else ""
  )
};

(:--------------------------------------------------------------------------------------------------:)

(: generate sequence of non-type property/value pair strings :)
declare function page:property-value-pairs($IRIs,$columnInfo,$record,$id,$serialization,$namespaces)
{
  (: generates property/value pairs that have fixed values :)
  for $columnType in $columnInfo
  where "$constant" = $columnType/header/text() and $columnType/subject_id/text() = $id
  return switch ($columnType/type/text())
     case "plain" return page:plain-literal($columnType/predicate/text(),$columnType/value/text(),$serialization)
     case "datatype" return page:datatyped-literal($columnType/predicate/text(),$columnType/value/text(),$columnType/attribute/text(),$serialization,$namespaces)
     case "language" return page:language-tagged-literal($columnType/predicate/text(),$columnType/value/text(),$columnType/attribute/text(),$serialization)
     case "iri" return page:iri($columnType/predicate/text(),$columnType/value/text(),$serialization,$namespaces)
     default return ""
,

  (: generates property/value pairs whose values are given in the metadata table :)
  for $column in $record/child::*, $columnType in $columnInfo
  (: The loop only includes columns containing properties associated with the class of the described resource; that column in the record must not be empty :)
  where fn:local-name($column) = $columnType/header/text() and $columnType/subject_id/text() = $id and $column//text() != ""
  return switch ($columnType/type/text())
     case "plain" return page:plain-literal($columnType/predicate/text(),$column//text(),$serialization)
     case "datatype" return page:datatyped-literal($columnType/predicate/text(),$column//text(),$columnType/attribute/text(),$serialization,$namespaces)
     case "language" return page:language-tagged-literal($columnType/predicate/text(),$column//text(),$columnType/attribute/text(),$serialization)
     case "iri" return 
       (:: check whether the value column in the mapping table has anything in it :)
       if ($columnType/value/text())
       then
         (: something is there. Construct the IRI by concatenating what's in the value column, the column content, and what's in the attribute column :)
         page:iri($columnType/predicate/text(),$columnType/value/text()||$column//text()||$columnType/attribute/text(),$serialization,$namespaces)
       else
         (: nothing is there.  The column either contains a full IRI or an abbreviated one :)
         page:iri($columnType/predicate/text(),$column//text(),$serialization,$namespaces)
     default return ""
,

  (: generates links to associated resources described in the same document :)
  for $columnType in $columnInfo
  where "$link" = $columnType/header/text() and $columnType/subject_id/text() = $id
  let $suffix := $columnType/value/text()
  return 
      for $iri in $IRIs
      where $iri/id/text()=$suffix
      let $object := $iri/fullId/text()
      return page:iri($columnType/predicate/text(),$object,$serialization,$namespaces)
};

(:--------------------------------------------------------------------------------------------------:)

(: this function closes the root container for the serialization (if any) :)
declare function page:close-container($serialization)
{  
switch ($serialization)
    case "turtle" return ""
    case "xml" return "</rdf:RDF>&#10;"
    case "json" return ']&#10;}'
    default return ""
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:construct-iri($baseIRI,$classes)
{
  (: This function basically creates a parallel set of class records that contain the full URIs in addition to the abbreviated ones that are found in classes.csv . In addition, UUID blank node identifiers are generated for nodes that are anonymous.  UUIDs are used instead of sequential numbers since the main function may be hacked to serialize ALL records rather than just one and in that case using UUIDs would ensure that there is no duplication of blank node identifiers among records. :)
  for $class in $classes
  let $suffix := $class/id/text()
  return
     <record>{
     if (fn:substring($suffix,1,2)="_:")
     then (<fullId>{concat("_:",random:uuid() ) }</fullId>, $class/id, $class/class )
     else 
       if ($suffix="$root")
       then (<fullId>{$baseIRI}</fullId>, $class/id, $class/class )
       else (<fullId>{concat($baseIRI,$suffix) }</fullId>, $class/id, $class/class )
   }</record>
};

(:--------------------------------------------------------------------------------------------------:)

declare function page:html($id,$serialization)
{
 let $value := concat("Placeholder page for local ID=",$id,".")
return 
<html>
  <body>
  {$value}
  </body>
</html>
};

(: Code from https://raw.githubusercontent.com/baskaufs/guid-o-matic/master/propvalue.xqm :)

(: Note: copied this function from http://www.xqueryfunctions.com/xq/functx_chars.html :)
declare function page:chars
  ( $arg as xs:string? )  as xs:string* {

   for $ch in string-to-codepoints($arg)
   return codepoints-to-string($ch)
 } ;

declare function page:escape-bad-characters($string,$serialization)
{
switch ($serialization)
    case "json"
    case "turtle" 
       return fn:replace(
                       fn:replace($string,'\\','\\\\')
                       ,'"','\\"')
              
    case "xml"
       return page:escape-less-than(
                       fn:replace($string,'&amp;','&amp;amp;')
                      )
    default return $string
};

declare function page:escape-less-than($string)
{
string-join(
for $char in page:chars($string)
return 
  if ($char = '<') then
     ``[&lt;]``
  else
     $char
 )
};

declare function page:expand-iri($abbreviated,$namespaces)
{
  (: if the passed URI is already expanded as an HTTP IRI or a URN, the function does nothing :)
if (fn:substring($abbreviated,1,8)="https://")
then 
  $abbreviated
else
  if (fn:substring($abbreviated,1,7)="http://")
  then 
    $abbreviated
  else
    if (fn:substring($abbreviated,1,4)="urn:")
    then 
      $abbreviated
    else
      let $curie := substring-before($abbreviated,":")
      let $localName := substring-after($abbreviated,":")
      for $namespace in $namespaces
      where $namespace/curie/text()=$curie
      return concat($namespace/value/text(),$localName)
};

declare function page:wrap-turtle-iri($iri)
{
  (: check whether an unabbreviated HTTP IRI or URN. If so, wrap in lt/gt brackets.  If not, do nothing :)
  if (fn:substring($iri,1,8)="https://")
  then 
    concat('<',$iri,">")
  else
    if (fn:substring($iri,1,7)="http://")
    then 
      concat('<',$iri,">")
    else
      if (fn:substring($iri,1,4)="urn:")
      then 
        concat('<',$iri,">")
      else
        $iri
};

declare function page:subject($iri,$serialization)
{
  (: Note: the subject iri begins the description, so the returned string includes characters necessary to open the container.  In turtle and xml, blank nodes have different formats than full URIs :)
switch ($serialization)
  case "turtle" return 
       if (fn:substring($iri,1,2)="_:") 
       then concat($iri,"&#10;") 
       else concat("<",$iri,">&#10;")
  case "xml" return 
       if (fn:substring($iri,1,2)="_:") 
       then concat('<rdf:Description rdf:nodeID="',concat("U",fn:substring($iri,3,fn:string-length($iri)-2)),'">&#10;') 
       else concat('<rdf:Description rdf:about="',$iri,'">&#10;')
  case "json" return concat("{&#10;",'"@id": "',$iri,'",&#10;')
  default return ""
};

declare function page:plain-literal($predicate,$dirtyString,$serialization)
{
let $string := page:escape-bad-characters($dirtyString,$serialization)
return switch ($serialization)
  case "turtle" return concat("     ",$predicate,' "',$string,'";&#10;')
  case "xml" return concat("     <",$predicate,'>',$string,'</',$predicate,'>&#10;')
  case "json" return concat('"',$predicate,'": "',$string,'",&#10;')
  default return ""
};

declare function page:datatyped-literal($predicate,$dirtyString,$datatype,$serialization,$namespaces)
{
let $string := page:escape-bad-characters($dirtyString,$serialization)
return switch ($serialization)
  case "turtle" return concat("     ",$predicate,' "',$string,'"^^',page:wrap-turtle-iri($datatype),";&#10;")
  case "xml" return concat("     <",$predicate,' rdf:datatype="',page:expand-iri($datatype,$namespaces),'">',$string,'</',$predicate,'>&#10;')
  case "json" return concat('"',$predicate,'": {"@type": "',$datatype,'","@value": "',$string,'"},&#10;')
  default return ""
};

declare function page:language-tagged-literal($predicate,$dirtyString,$lang,$serialization)
{
let $string := page:escape-bad-characters($dirtyString,$serialization)
return switch ($serialization)
  case "turtle" return concat("     ",$predicate,' "',$string,'"@',$lang,";&#10;")
  case "xml" return concat("     <",$predicate,' xml:lang="',$lang,'">',$string,'</',$predicate,'>&#10;')
  case "json" return concat('"',$predicate,'": {"@language": "',$lang,'","@value": "',$string,'"},&#10;')
  default return ""
};

declare function page:iri($predicate,$string,$serialization,$namespaces)
{
switch ($serialization)
  case "turtle" return concat("     ",$predicate,' ',page:wrap-turtle-iri($string),";&#10;") 
  case "xml" return 
       if (fn:substring($string,1,2)="_:") 
       then concat("     <",$predicate,' rdf:nodeID="',concat("U",fn:substring($string,3,fn:string-length($string)-2)),'"/>&#10;') 
       else concat("     <",$predicate,' rdf:resource="',page:expand-iri($string,$namespaces),'"/>&#10;')
  case "json" return concat('"',$predicate,'": {"@id": "',$string,'"},&#10;')
  default return ""
};

declare function page:type($type,$serialization,$namespaces)
{
  (: Note: type is the last property listed, so the returned string includes characters necessary to close the container :)
  (: There also is no trailing separator (if the serialization has one). :) 
  (: A value of "null" suppresses declaring a type and simply closes the container. :)
switch ($serialization)
  case "turtle" return
      if ($type = "null")
      then "&#10;"
      else concat("     a ",page:wrap-turtle-iri($type),".&#10;&#10;")
  case "xml" return
      if ($type = "null")
      then '</rdf:Description>&#10;&#10;'
      else  concat('     <rdf:type rdf:resource="',page:expand-iri($type,$namespaces),'"/>&#10;</rdf:Description>&#10;&#10;')
  case "json" return
      if ($type = "null")
      then "}&#10;"
      else  concat('"@type": "',$type,'"&#10;',"}&#10;")
  default return ""
};

declare function page:media-type($serialization)
{
switch ($serialization)
  case "turtle" return "text/turtle"
  case "xml" return "application/rdf+xml"
  case "json" return "application/json"
  default return ""
};

declare function page:extension($serialization)
{
switch ($serialization)
  case "turtle" return ".ttl"
  case "xml" return ".rdf"
  case "json" return ".json"
  default return ""
};

declare function page:extract-html-header($headers)
{
let $result :=  
  for $header in $headers 
  return if (contains($header, "text/html")) 
    then true() 
    else false()
return if ($result = true()) 
  then "text/html" 
  else $headers
};
