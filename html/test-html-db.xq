xquery version "3.1";
(: part of Guid-O-Matic 2.0 https://github.com/baskaufs/guid-o-matic :)(: part of Guid-O-Matic 2.0 https://github.com/baskaufs/guid-o-matic . You are welcome to reuse or hack in any way :)

import module namespace html = 'http://rs.tdwg.com/html' at './html.xqm';

let $db := "terms"
return html:generate-list($db)


