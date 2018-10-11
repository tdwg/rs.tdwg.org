xquery version "3.1";
(: part of Guid-O-Matic 2.0 https://github.com/baskaufs/guid-o-matic . You are welcome to reuse or hack in any way :)

import module namespace page = 'http://basex.org/modules/web-page' at './restxq.xqm';

page:handle-html("dwctype","Taxon")