FROM basex/basexhttp:9.1
LABEL maintainer="mblissett@gbif.org"

USER root
RUN apk update && apk add --no-cache python3 py3-requests supervisor varnish shadow

# Use a different directory for BaseX, because the /srv directory is declared a non-persistent volume.
RUN cp -pr /srv /basex
RUN usermod -d /basex basex
WORKDIR /basex

# BaseX password and script
COPY basex/users.xml /basex/basex/data
COPY html/restxq.xqm /basex/basex/webapp

# Initialize the database (starts up, imports data, shuts down)
RUN mkdir -p /usr/src/rs.tdwg.org
COPY . /usr/src/rs.tdwg.org
USER basex
RUN /usr/src/rs.tdwg.org/docker/initialize-database.sh tdwg/rs.tdwg.org/ master '' http://localhost:8984/rest/ xxxxxxxxxxxxxxxxxx
USER root
RUN rm -Rf /usr/src/rs.tdwg.org

COPY docker/supervisord.conf /etc/supervisord.conf
COPY docker/varnish_default.vcl /etc/varnish/default.vcl

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
