package policy.ingress

import future.keywords
import input.attributes.request.http as http_request
# Add policy/rules to allow or deny ingress traffic

default allow = false

issuer   := "https://twdpsio.us.auth0.com/"
audience := "w47MtsmRGb3DDTKqWdXMy9L7KudD5nDq"
current_time := time.now_ns()

metadata_discovery(iss) = http.send({
    "url": concat("", [iss, ".well-known/openid-configuration"]),
    "method": "GET",
    "force_cache": true,
    "force_cache_duration_seconds": 86400 # Cache response for 24 hours
}).body

metadata := metadata_discovery(issuer)

jwks_endpoint := metadata.jwks_uri

jwks_request(url) = http.send({
    "url": url,
    "method": "GET",
    "force_cache": true,
    "force_cache_duration_seconds": 3600 # Cache response for an hour
})

jwks := jwks_request(jwks_endpoint).raw_body

decoded_token := io.jwt.decode(bearer_token)[1]

is_valid := io.jwt.verify_rs256(bearer_token, jwks)
is_not_expired {
    expires_nanoseconds := decoded_token["exp"]*1000000000
    expires_nanoseconds > current_time
}
now_is_after_issued_at {
    issued_at_nanoseconds := decoded_token["iat"]*1000000000
    issued_at_nanoseconds <= current_time
}
is_our_issuer {
    decoded_token["iss"] == issuer
}

bearer_token := t {
    # Bearer tokens are contained inside of the HTTP Authorization header. This rule
    # parses the header and extracts the Bearer token value. If no Bearer token is
    # provided, the `bearer_token` value is undefined.
    v := http_request.headers.authorization
    startswith(v, "Bearer ")
    t := substring(v, count("Bearer "), -1)
}

allow {
    is_valid
    is_not_expired
    now_is_after_issued_at
    is_our_issuer
}
