xquery version "3.1";

module namespace html = 'http://rs.tdwg.com/html';

(:--------------------------------------------------------------------------------------------------:)

declare function html:generate-list($db)
{
let $constants := fn:collection($db)//constants/record
let $baseIriColumn := $constants//baseIriColumn/text()

let $metadata := fn:collection($db)/metadata/record
  

let $message := "here is some text"
return 
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Test generated web page</title>
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
