# Deployment

The server is deployed as a Docker image to a GCS micro instance.

The production deployment is managed by GBIF, but anyone can use Docker to run the server locally:

1. Install Docker.

2. Run the production image: `docker run -ti --publish 1984:1984 --publish 8984:8984 gcr.io/rs-tdwg-org/basex:latest`

3. (You probably don't know the admin password, which is not the default.)

Alternatively, rebuild the image and run that:

1. Optionally, edit `Dockerfile` — for example, comment out the `users.xml` line, so the server uses the default `admin:admin` user and password.

2. From this directory, run `docker build -t rs-tdwg-org-basex .`

3. Run the image: `docker run -ti --publish 1984:1984 --publish 8984:8984 rs-tdwg-org-basex`

Either way, you can then test with an HTTP query:

```
curl -SsiL -H 'Accept: text/turtle' http://192.0.2.1:8984/dwc/terms/recordedBy
```
