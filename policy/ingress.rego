
package policy.ingress

import future.keywords
import input.attributes.request.http as http_request
# Add policy/rules to allow or deny ingress traffic

default allow = false

issuer   := "https://twdpsio.us.auth0.com/"
audience := "w47MtsmRGb3DDTKqWdXMy9L7KudD5nDq"

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

is_valid := io.jwt.decode_verify(bearer_token, {
        "time": time.now_ns(),
        "aud": audience,
        "cert": jwks,
        "iss": issuer
    })[0]

bearer_token := t {
	# Bearer tokens are contained inside of the HTTP Authorization header. This rule
	# parses the header and extracts the Bearer token value. If no Bearer token is
	# provided, the `bearer_token` value is undefined.
	v := http_request.headers.authorization
	startswith(v, "Bearer ")
	t := substring(v, count("Bearer "), -1)
}

allow {
    print(input.attributes)
    is_valid
}
