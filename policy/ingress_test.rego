package policy.ingress

import future.keywords

mock_decode(x) := [{}, x, {}]
mock_verify_rs256("my-jwt", _) := true
mock_verify_rs256(x, _)        := false if x != "my-jwt"
time_now_ns(x) := x

test_valid_jwt_is_allowed {
  is_valid
    with input.attributes.request.http.headers.authorization as "Bearer my-jwt"
    #with io.jwt.decode as mock_decode
    with io.jwt.verify_rs256 as mock_verify_rs256
}

test_invalid_jwt_not_allowed {
  not is_valid
    with input.attributes.request.http.headers.authorization as "Bearer I-Am-Bad"
    with io.jwt.decode as mock_decode
}

test_wrong_issuer_is_not_allowed {
  not is_our_issuer
    with decoded_token as {"iss": "some-bad-issuer"}
}

test_is_our_issuer_is_valid {
  is_our_issuer
    with decoded_token as {"iss": "https://twdpsio.us.auth0.com/"}
}

test_is_not_expired {
  is_not_expired
    with decoded_token as {"exp": 1661185050}
    with time.now_ns as time_now_ns(1661185040000000000)
}

test_is_expired {
  not is_not_expired
    with decoded_token as {"exp": 1661185050}
    with time.now_ns as time_now_ns(1661185060000000000)
}

test_is_after_issued_at {
  now_is_after_issued_at
    with decoded_token as {"iat": 1661185050}
    with time.now_ns as time_now_ns(1661185060000000000)
}

test_is_not_after_issued_at {
  not now_is_after_issued_at
    with decoded_token as {"iat": 1661185050}
    with time.now_ns as time_now_ns(1661185040000000000)
}

test_is_allowed_with_criteria {
  allow
    with is_valid as true
    with is_not_expired as true
    with now_is_after_issued_at as true
    with is_our_issuer as true
}

test_is_not_allowed_if_not_valid {
  not allow
    with is_valid as false
    with is_not_expired as true
    with now_is_after_issued_at as true
    with is_our_issuer as true
}

test_is_not_allowed_if_is_expired {
  not allow
    with is_valid as true
    with is_not_expired as false
    with now_is_after_issued_at as true
    with is_our_issuer as true
}

test_is_not_allowed_if_before_issued_at {
  not allow
    with is_valid as true
    with is_not_expired as true
    with now_is_after_issued_at as false
    with is_our_issuer as true
}

test_is_not_allowed_if_is_not_our_issuer {
  not allow
    with is_valid as true
    with is_not_expired as true
    with now_is_after_issued_at as true
    with is_our_issuer as false
}
