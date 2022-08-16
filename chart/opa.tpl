- name: opa
  image: openpolicyagent/opa:0.42.2-envoy-rootless
  volumeMounts:
    - readOnly: true
      mountPath: /config
      name: opa-config-vol
  livenessProbe:
    httpGet:
      path: /health
      scheme: HTTP
      port: 8282
    initialDelaySeconds: 5    # Tune these periods for your environemnt
    periodSeconds: 5
  readinessProbe:
    httpGet:
      path: /health?bundle=true # Include bundle activation in readiness
      scheme: HTTP
      port: 8282
    initialDelaySeconds: 5
    periodSeconds: 5
  args:
    - "run"
    - "--server"
    - "--ignore=.*"
    - "--config-file=/config/conf.yaml"
    - "--authorization=basic"
    - "--addr=http://127.0.0.1:8181"
    - "--diagnostic-addr=0.0.0.0:8282"
