xquery version "3.1";

module namespace html = 'http://rs.tdwg.com/html';

(: In order to avoid hard-coding file locations, the propvalue module is imported from GitHub.  It is unlikely that you will need to modify any of the functions it contains, but if you do, you will need to substitute after the "at" keyword the path to the local directory where you put the propvalue.xqm file :)
import module namespace propvalue = 'http://bioimages.vanderbilt.edu/xqm/propvalue' at 'https://raw.githubusercontent.com/baskaufs/guid-o-matic/master/propvalue.xqm'; 

(:--------------------------------------------------------------------------------------------------:)

declare function html:dwc()
{
let $message := "here is some text"
return 
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Test generated web page</title>
  </head>
  <body>
    {$message}
  </body>
</html>
};
