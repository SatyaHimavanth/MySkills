# Observability — Production

## Purpose
Provide centralized signals that let operators diagnose traffic, latency, failures, and dependency saturation.

## Required signals

At minimum:

```text
traffic
latency
errors
saturation
```

Also expose useful dependency signals:

```text
DB connection pressure
Redis latency/errors
queue depth
cache hit/miss
external API latency/errors
rate-limit rejections
```

## Logging

- structured logs
- stable field names
- request/trace correlation
- no credentials, tokens, passwords, or raw sensitive payloads
- centralized collection

## Tracing

Use OpenTelemetry traces when distributed diagnosis is valuable. Configure exporters and sampling through typed settings, not hard-coded endpoints. [OpenObserve](https://github.com/openobserve/openobserve) is one viable self-hosted OTLP-native destination for logs+metrics+traces in one system (AGPL-3.0 — review before embedding/redistributing; not a concern for internal-only use). Not exclusive: any OTLP-compatible backend works without app code changes since the SDK only talks to a configured endpoint.

## Metrics

Use low-cardinality labels and histograms for latency. Avoid labels such as request IDs or arbitrary user IDs.

## Alerting inputs

Useful alert signals include:

- elevated 5xx rate
- p95/p99 latency degradation
- DB pool exhaustion
- dependency outage
- queue backlog
- repeated readiness failures

Telemetry export failure should not block normal request processing indefinitely.

## Privacy and retention

Telemetry is operational data. Apply retention, access control, redaction, and PII-minimization rules.
