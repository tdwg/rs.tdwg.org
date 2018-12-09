(: this module needs to be put in the webapp folder of your BaseX installation.  On my local computer it's at c:\Program Files (x86)\BaseX\webapp\ On the Tomcat installation, it's at opt/tomcat/webapps/gom/restxq.xqm, where gom is the context under which the BaseX server is running :)

module namespace page = 'http://basex.org/modules/web-page';
import module namespace serialize = 'http://bioimages.vanderbilt.edu/xqm/serialize' at 'https://raw.githubusercontent.com/baskaufs/guid-o-matic/master/serialize.xqm';
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
  page:see-also($acceptHeader,"/index","index",page:subdomain()||"index")
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
                  serialize:main-github("",$flag,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/",$stripped-local-name,"dump","false")
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
  let $metadataDoc := http:send-request(<http:request method='get' href='{"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/index/index-datasets.csv"}'/>)[2]
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
      let $lookup-string := page:subdomain()||$vocab||"/doc/"||$stripped-local-name||"/"
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||$vocab||"/doc/"||$local-id||"/"
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
      let $lookup-string := page:subdomain()||$vocab||"/doc/"||$local-id||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||$vocab||"/doc/"||$local-id||"/"||$date
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
      let $lookup-string := page:subdomain()||"dwc/terms/guides/"||$stripped-local-name||"/"
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||"dwc/terms/guides/"||$local-id||"/"
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
      let $lookup-string := page:subdomain()||"dwc/terms/simple/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||"dwc/terms/simple/"||$date
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
      let $lookup-string := page:subdomain()||"dwc/terms/namespace/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||"dwc/terms/namespace/"||$date
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
      let $lookup-string := page:subdomain()||"dwc/terms/guides/"||$local-id||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||"dwc/terms/guides/"||$local-id||"/"||$date
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
      let $lookup-string := page:subdomain()||$stripped-local-name||"/"
      return
      switch ($stripped-local-name)
        (: handle the special case of TDWG decisions :)
        case "decisions" return page:handle-repesentation($acceptHeader,$extension,"term-lists",page:subdomain()||"decisions/")
        (: handle the special case of the dataset index :)
        case "index" return page:handle-repesentation($acceptHeader,$extension,"index",page:subdomain()||"index")
        default return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||$local-id||"/"
      let $redirect-id := "/"||$local-id
      return
      switch ($local-id)
        (: handle the special case of TDWG decisions :)
        case "decisions" return page:see-also($acceptHeader,"/decisions","term-lists",page:subdomain()||"decisions/")
        (: handle the special case of the simple Darwin Core guide :)
        case "index" return page:see-also($acceptHeader,"/index","index",page:subdomain()||"index")
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
      let $lookup-string := page:subdomain()||"version/"||$vocab||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||"version/"||$vocab||"/"||$local-id
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
      let $lookup-string := page:subdomain()||$namespace||"/"||$stripped-local-name||"/"
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||$namespace||"/"||$local-id||"/"
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
      let $lookup-string := page:subdomain()||$vocab||"/version/"||$term-list||"/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||$vocab||"/version/"||$term-list||"/"||$local-id
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
      let $lookup-string := page:subdomain()||"dwc/version/terms/attributes/"||$stripped-local-name
      return page:handle-repesentation($acceptHeader,$extension,$db,$lookup-string)
    else
      (: no extension :)
      let $lookup-string := page:subdomain()||"dwc/version/terms/attributes/"||$local-id
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
  let $termlistFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/term-lists/term-lists.csv"
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
  let $termlistFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/term-lists/term-lists.csv"
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
        case "attributes" return page:handle-repesentation($acceptHeader,$extension,"term-lists",page:subdomain()||"dwc/terms/attributes/")
        (: handle the special case of the simple Darwin Core guide :)
        case "simple" return page:handle-repesentation($acceptHeader,$extension,"docs",page:subdomain()||"dwc/terms/simple/")
        (: handle the special case of the Darwin Core namespace policy :)
        case "namespace" return page:handle-repesentation($acceptHeader,$extension,"docs",page:subdomain()||"dwc/terms/namespace/")
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
        case "attributes" return page:see-also($acceptHeader,"/dwc/terms/attributes","term-lists",page:subdomain()||"dwc/terms/attributes/")
        (: handle the special case of the simple Darwin Core guide :)
        case "simple" return page:see-also($acceptHeader,"/dwc/terms/simple","docs",page:subdomain()||"dwc/terms/simple/")
       (: handle the special case of the Darwin Core namespace policy :)
        case "namespace" return page:see-also($acceptHeader,"/dwc/terms/namespace","docs",page:subdomain()||"dwc/terms/namespace/")
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

declare %rest:path("/tapir/1.0/{$path=.+}") function page:tapir10-redirect($path)
 {<rest:redirect>{"https://raw.githubusercontent.com/tdwg/tapir/1.0/"||$path}</rest:redirect>};
:)
(: This particular URL seems to be in use and redirects to this particular place :)
declare %rest:path("/tapir/1.0/schema/tdwg_tapir.xsd") function page:tapir10-tdwgtapir-redirect()
 {<rest:redirect>{"https://raw.githubusercontent.com/tdwg/infrastructure/master/rs.tdwg.org/tapir/1.0/schema/tapir.xsd"}</rest:redirect>};

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
 {<rest:redirect>{"https://dwc.tdwg.org/xsd/"||$path}</rest:redirect>};

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
  if (serialize:find-github($lookup-string,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/",$db))  (: check whether the resource is in the database :)
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
      case "index" return page:temp-redirect("https://github.com/tdwg/rs.tdwg.org/blob/master/README.md","")
      default return page:handle-html($db,$lookup-string)
  else
  (: I moved this within the ELSE statement because it interferes with the HTML redirect if I leave it before the IF :)
  <rest:response>
    <output:serialization-parameters>
      <output:media-type value='{$response-media-type}'/>
    </output:serialization-parameters>
  </rest:response>,
  serialize:main-github($lookup-string,$flag,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/",$db,"single","false")
};

(: Function to return a web page for vocabs etc. :)
declare function page:handle-html($db,$lookup-string)
{
let $redirectFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/html/redirects.csv"
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
let $redirectFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/docs/docs.csv"
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
let $redirectFilePath := "https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/docs-versions/docs-versions.csv"
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
  if(serialize:find-github($lookup-string,"https://raw.githubusercontent.com/tdwg/rs.tdwg.org/"||page:branch()||"/",$db))  (: check whether the resource is in the database :)
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

declare function page:subdomain()
{
  normalize-space(http:send-request(<http:request method='get' href='https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/html/subdomain.txt'/>)[2])
};

declare function page:branch()
{
  normalize-space(http:send-request(<http:request method='get' href='https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/html/branch.txt'/>)[2])
};