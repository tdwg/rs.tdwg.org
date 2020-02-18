FROM basex/basexhttp:9.1
LABEL maintainer="mblissett@gbif.org"

COPY basex/users.xml /srv/basex/data
COPY html/restxq.xqm /srv/basex/webapp

USER root
RUN apk update && apk add --no-cache python3 py3-requests

RUN mkdir -p /usr/src/rs.tdwg.org
COPY . /usr/src/rs.tdwg.org
USER basex

# Initialize the database (starts up, imports data, shuts down)
RUN /usr/src/rs.tdwg.org/docker/initialize-database.sh tdwg/rs.tdwg.org/ master '' http://localhost:8984/rest/ vPgaimZmAFibyF9tWK3F-VXL
