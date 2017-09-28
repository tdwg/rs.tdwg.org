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
    <p>{
      (: check records in the database for a match to the requested URI :)
      for $record in $metadata
      where $record/*[local-name()=$baseIriColumn]/text()="recordedBy"
      return $record/label/text()     
    }</p>
  </body>
</html>
};
