package policy.ingress

mock_decode(x) := [{}, x, {}]
mock_verify_rs256("my-jwt", _) := true
time_now_ns(x) := x

test_valid_jwt_is_allowed {
  data.policy.ingress.is_valid
    with input.attributes.request.http.headers.authorization as "Bearer my-jwt"
    with io.jwt.verify_rs256 as mock_verify_rs256
}

test_invalid_jwt_not_allowed {
  not data.policy.ingress.is_valid
    with input.attributes.request.http.headers.authorization as "Bearer I-Am-Bad"
    with io.jwt.decode as mock_decode
}

test_wrong_issuer_is_not_allowed {
  not data.policy.ingress.is_our_issuer
    with data.decoded_token as {"iss": "some-bad-issuer"}
}

test_is_our_issuer_is_valid {
  data.policy.ingress.is_our_issuer
    with data.policy.ingress.decoded_token as {"iss": "https://twdpsio.us.auth0.com/"}
}

test_is_not_expired {
  data.policy.ingress.is_not_expired
    with data.policy.ingress.decoded_token as {"exp": 1661185050}
    with time.now_ns as time_now_ns(1661185040000000000)
}

test_is_expired {
  not data.policy.ingress.is_not_expired
    with data.policy.ingress.decoded_token as {"exp": 1661185050}
    with time.now_ns as time_now_ns(1661185060000000000)
}

test_is_after_issued_at {
  data.policy.ingress.now_is_after_issued_at
    with data.policy.ingress.decoded_token as {"iat": 1661185050}
    with time.now_ns as time_now_ns(1661185060000000000)
}

test_is_not_after_issued_at {
  not data.policy.ingress.now_is_after_issued_at
    with data.policy.ingress.decoded_token as {"iat": 1661185050}
    with time.now_ns as time_now_ns(1661185040000000000)
}

test_is_allowed_with_criteria {
  data.policy.ingress.allow
    with data.policy.ingress.is_valid as true
    with data.policy.ingress.is_not_expired as true
    with data.policy.ingress.now_is_after_issued_at as true
    with data.policy.ingress.is_our_issuer as true
}

test_is_not_allowed_if_not_valid {
  not data.policy.ingress.allow
    with data.policy.ingress.is_valid as false
    with data.policy.ingress.is_not_expired as true
    with data.policy.ingress.now_is_after_issued_at as true
    with data.policy.ingress.is_our_issuer as true
}

test_is_not_allowed_if_is_expired {
  not data.policy.ingress.allow
    with data.policy.ingress.is_valid as true
    with data.policy.ingress.is_not_expired as false
    with data.policy.ingress.now_is_after_issued_at as true
    with data.policy.ingress.is_our_issuer as true
}

test_is_not_allowed_if_before_issued_at {
  not data.policy.ingress.allow
    with data.policy.ingress.is_valid as true
    with data.policy.ingress.is_not_expired as true
    with data.policy.ingress.now_is_after_issued_at as false
    with data.policy.ingress.is_our_issuer as true
}

test_is_not_allowed_if_is_not_our_issuer {
  not data.policy.ingress.allow
    with data.policy.ingress.is_valid as true
    with data.policy.ingress.is_not_expired as true
    with data.policy.ingress.now_is_after_issued_at as true
    with data.policy.ingress.is_our_issuer as false
}
