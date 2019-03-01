FROM basex/basexhttp:9.1
LABEL maintainer="mblissett@gbif.org"

COPY basex/users.xml /srv/basex/data
COPY html/restxq.xqm /srv/basex/webapp
