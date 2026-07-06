FROM alpine:3
LABEL maintainer="mblissett@gbif.org"

RUN apk update && apk add --no-cache openjdk8 curl unzip bash python3 py3-requests && \
    adduser -h /basex -D -u 1984 basex
RUN curl --fail --output /BaseX91.zip https://files.basex.org/releases/9.1/BaseX91.zip && \
    unzip -d /basex /BaseX91.zip && \
    rm /BaseX91.zip && \
    chown -R basex /basex
EXPOSE 8984

USER root
WORKDIR /basex

# Initialize the database (sets password, starts up, imports data, shuts down)
COPY . /usr/src/rs.tdwg.org
RUN rm -Rf /usr/src/rs.tdwg.org/.git
USER basex
RUN /usr/src/rs.tdwg.org/docker/initialize-database.sh ../ '' http://localhost:8984/rest/
USER root

# BaseX script
COPY html/restxq.xqm /basex/basex/webapp

ENV HOME=/basex
CMD ["/basex/basex/bin/basexhttp"]
