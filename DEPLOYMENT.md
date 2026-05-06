[![Build Status](https://builds.gbif.org/job/tdwg-rs/badge/icon)](https://builds.gbif.org/job/tdwg-rs/)

# Deployment

The server is deployed as a Docker image.

## Public use of the image

The production deployment is managed by GBIF, but anyone can use Docker to run the server locally:

1. Install Docker.

2. Build the Docker image: `docker build -t rs-tdwg-org .`

3. Run the image: `docker run -ti --publish 8984:8984 rs-tdwg-org`

You can then test with an HTTP query:

```
curl -SsiL -H 'Accept: text/turtle' http://localhost:8984/dwc/terms/recordedBy
```

## Actual deployment

Changes to the `master` branch on GitHub are tracked by the [build system](https://builds.gbif.org/job/tdwg-rs/),
which will rebuild the Docker container and refresh the container running on http://test.rs.tdwg.org/.

GitHub releases are also tracked by the build system, and will result in a versioned Docker container being built
and stored in GBIF's Docker repository, and that version being deployed to http://rs.tdwg.org/.

Specific branches on this repository can also be tracked and deployed, for example to aid generating metadata
for a public review.  These branches are currently enabled:

* `bdq`, deployed at http://bdq-public-review.rs.tdwg.org/
* `mids`, deployed at http://mids-public-review.rs.tdwg.org/

If you need a new branch to be deployed, create an issue in this repository.

*In all cases, HTTPS URLs are also supported.*
