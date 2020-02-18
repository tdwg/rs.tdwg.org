# Deployment

The server is deployed as a Docker image to a GBIF development server.

## Public use of the image

The production deployment is managed by GBIF, but anyone can use Docker to run the server locally:

1. Install Docker.

2. Run the production image: `docker run -ti --publish 1984:1984 --publish 8984:8984 gcr.io/rs-tdwg-org/basex:latest`

3. (You probably don't know the admin password, which is not the default.)

## Rebuilding the image for private use

Alternatively, rebuild the image and run that:

1. Optionally, edit `Dockerfile` — for example, comment out the `users.xml` line, so the server uses the default `admin:admin` user and password.

2. From this directory, run `docker build -t rs-tdwg-org-basex .`

3. Run the image: `docker run -ti --publish 1984:1984 --publish 8984:8984 rs-tdwg-org-basex`

Either way, you can then test with an HTTP query:

```
curl -SsiL -H 'Accept: text/turtle' http://192.0.2.1:8984/dwc/terms/recordedBy
```

## Actual deployment

The real build to the GCS micro instance uses:
```
docker build -t gcr.io/rs-tdwg-org/basex . && docker push gcr.io/rs-tdwg-org/basex
```
Then reset the instance (from [https://console.cloud.google.com/compute/instances?project=rs-tdwg-org](VM instances) choose "Reset"), and maybe have a look:
```
gcloud compute --project "rs-tdwg-org" ssh --zone "us-east1-b" "rs-tdwg-org-basex"
```

Then, until the firewall is updated / BaseX is made to run on a different port, forward it to port 8080:
```
nohup socat tcp-listen:8080,reuseaddr,fork tcp:localhost:8984

curl -i http://tdwgrs-vh.tdwg.org:8984/dwc/terms/kingdom
```
