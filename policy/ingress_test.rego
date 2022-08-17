package policy.ingress

import future.keywords

mock_decode_verify("my-jwt", _) := [true, {}, {}]
# mock_decode_verify(x, _) := [false, {}, {}] if x != "my-jwt"

# in a test
## with data.jwks.cert as "mock-cert"
## with io.jwt.decode_verify as mock_decode_verify

test_issuer {
  input := {
  "attributes": {
    "request": {
      "http": {
        "headers": {
          "authorization": "Bearer my-jwt"
        }
      },
      "time": "2022-08-10T15:26:08.588079Z"
    }
  }
}
  allow
    with data.jwks.cert as "mock-cert"
    with input.attributes.request.http.headers.authorization as "Bearer my-jwt"
    # with input as input
    with io.jwt.decode_verify as mock_decode_verify
}



# test_allow if {
#     allow
#       with input.headers["x-token"] as "my-jwt"
#       with data.jwks.cert as "mock-cert"
#       with io.jwt.decode_verify as mock_decode_verify
# }

# app code
# allow if {
#     [true, _, _] = io.jwt.decode_verify(input.headers["x-token"], {"cert": cert, "iss": "corp.issuer.com"})
# }
