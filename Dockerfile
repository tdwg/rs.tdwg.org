FROM basex/basexhttp:9.1
LABEL maintainer="mblissett@gbif.org"

USER root
RUN apk update && apk add --no-cache python3 py3-requests supervisor varnish shadow

# Use a different directory for BaseX, because the /srv directory is declared a non-persistent volume.
RUN cp -pr /srv /basex
RUN usermod -d /basex basex
WORKDIR /basex

# BaseX password and script
COPY docker/basex-users.xml /basex/basex/data/users.xml
COPY html/restxq.xqm /basex/basex/webapp

# Initialize the database (starts up, imports data, shuts down)
COPY docker/ /usr/src/docker/
COPY index/ /usr/src/index/
USER basex
RUN /usr/src/docker/initialize-database.sh tdwg/rs.tdwg.org/ '' http://localhost:8984/rest/ xxxxxxxxxxxx
USER root
RUN rm -Rf /usr/src/docker /usr/src/index

COPY docker/supervisord.conf /etc/supervisord.conf
COPY docker/varnish_default.vcl /etc/varnish/default.vcl

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
