# Deployment

The server is deployed as a Docker image.

## Public use of the image

The production deployment is managed by GBIF, but anyone can use Docker to run the server locally:

1. Install Docker.

2. Run the production image: `docker run -ti --publish 80:80 gcr.io/rs-tdwg/basex:latest`

3. (You probably don't know the admin password, which is not the default.)

Publish the additional port `8984` if you wish to edit the database.

## Rebuilding the image for private use

Alternatively, rebuild the image and run that:

1. Edit `Dockerfile` — for example, comment out the `users.xml` line, so the server uses the default `admin:admin` user and password.

2. From this directory, run `docker build -t rs-tdwg-basex .`

3. Run the image: `docker run -ti --publish 80:80 rs-tdwg-basex`

Either way, you can then test with an HTTP query:

```
curl -SsiL -H 'Accept: text/turtle' http://192.0.2.1/dwc/terms/recordedBy
```

## Actual deployment

```
docker build -t gcr.io/rs-tdwg/basex . && docker push gcr.io/rs-tdwg/basex
```

Then either specify the Docker image for a GCE VM, or

```
docker run -ti --publish 80:80 gcr.io/rs-tdwg/basex:latest
```
