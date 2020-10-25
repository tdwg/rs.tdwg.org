[![Build Status](https://builds.gbif.org/job/tdwg-rs/badge/icon)](https://builds.gbif.org/job/tdwg-rs/)

# Deployment

The server is deployed as a Docker image.

## Public use of the image

The production deployment is managed by GBIF, but anyone can use Docker to run the server locally:

1. Install Docker.

2. Build the Docker image: `docker build -t rs-tdwg-org .`

3. Run the image: `docker run -ti --publish 80:80 rs-tdwg-org`

You can then test with an HTTP query:

```
curl -SsiL -H 'Accept: text/turtle' http://192.0.2.1/dwc/terms/recordedBy
```

## Actual deployment

Changes to the `master` branch on GitHub are tracked by the [build system](https://builds.gbif.org/job/tdwg-rs/), which will rebuild the
Docker container and refresh the container running on http://rs-test.tdwg.org/.

GitHub releases are also tracked by the build system, and will result in a versioned Docker container being built and stored in GBIF's
Docker repository, and that version being deployed to http://rs.tdwg.org/.
