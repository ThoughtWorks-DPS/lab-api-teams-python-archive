package policy.ingress

import future.keywords

mock_decode_verify("my-jwt", _) := [true, {}, {}]
mock_decode_verify(x, _)        := [false, {}, {}] if x != "my-jwt"
mock_time() := 1660619144000
mock_jwks() := "your-256-bit-shellecret"

test_valid_jwt_is_allowed {
  allow
    with input.attributes.request.http.headers.authorization as "Bearer my-jwt"
    with io.jwt.decode_verify as mock_decode_verify
}

test_invalid_jwt_not_allowed {
  not allow
    with input.attributes.request.http.headers.authorization as "Bearer I-Am-Bad"
    with io.jwt.decode_verify as mock_decode_verify
}

test_wrong_issuer_is_not_allowed {
  token_with_bad_issuer := "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3R3ZHBzaW8udXMuYXV0aDAuY29tLyIsInN1YiI6ImdpdGh1Ynw0NTQwMzUwOSIsImF1ZCI6Inc0N010c21SR2IzRERUS3FXZFhNeTlMN0t1ZEQ1bkRxIiwiaWF0IjoxNjYwNjE5MTQzLCJleHAiOjE2NjA2MjI3NDN9.RJG72DUBJ-O3Pc-zLmhv12XDXxnzautKFUEhw6YYmDA"

  not allow
    with input.attributes.request.http.headers.authorization as token_with_bad_issuer
    with time.now_ns as mock_time
}
