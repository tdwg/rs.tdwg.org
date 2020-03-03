vcl 4.0;

# Default backend definition. Set this to point to your content server.
backend default {
  .host = "localhost";
  .port = "8984";
}

sub vcl_recv {
  # Happens before we check if we have this in cache already.

  # Magic URL to Flush the entire cache
  if (req.url ~ "^/flush-cache") {
    ban("obj.status ~ .");
    return (synth(204, "Flushing everything on " + req.http.host));
  }

  if (req.method == "OPTIONS" || req.method == "HEAD" || req.method == "GET") {
    unset req.http.host;
    unset req.http.Cookie;
    return (hash);
  } else {
    return (synth(405, "Method Not Allowed"));
  }
}

sub vcl_hash {
  hash_data(req.url);
  hash_data(req.http.accept);

  return (lookup);
}

sub vcl_backend_response {
  # Happens after we have read the response headers from the backend.

  if (beresp.status <= 399) {
    set beresp.ttl = 4w;
    set beresp.http.Cache-Control = "public, max-age=3600";
  } else {
    set beresp.ttl = 30s;
    set beresp.http.Cache-Control = "public, max-age=30";
  }

  return(deliver);
}

sub vcl_deliver {
  # Happens when we have all the pieces we need, and are about to send the response.
}
