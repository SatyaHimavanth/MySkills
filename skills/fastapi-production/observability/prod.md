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

## Choosing a backend by use case

Instrumentation stays vendor-neutral (OTLP) regardless of choice — this table is about where the data goes, not how it's collected:

| Situation | Open source / self-hosted | Paid / managed |
|---|---|---|
| Cost-sensitive, small-to-mid team, OK operating it yourself | [OpenObserve](https://github.com/openobserve/openobserve) — single binary/Helm chart, object-storage backed (S3/GCS/Azure Blob), no per-host/per-seat fees. AGPL-3.0 (see `local_dev.md`'s licensing note) | — |
| OpenTelemetry-native, want a self-hosted Datadog-shaped UX without per-host billing | [SigNoz](https://github.com/SigNoz/signoz) — free if self-hosted, built OTel-first | — |
| Already standardized on Prometheus/Grafana dashboards, want the classic OSS stack | Grafana Stack (Loki + Tempo + Mimir + Grafana, the "LGTM" stack) — most operational components to run of the self-hosted options | Grafana Cloud — same stack, managed, less ops overhead than self-hosting it |
| Want one platform for everything (metrics/traces/logs/RUM/synthetics), budget allows, minimizing tool sprawl matters most | — | Datadog — broadest integrations and correlation UX; commonly the most expensive at scale, turn on cost controls from day one |
| Debugging "why is this *one* request slow" in a high-cardinality system is the actual hard problem, not infra breadth | — | Honeycomb — built specifically for high-cardinality event exploration, narrower scope than a full platform |
| Want predictable pricing, solid APM, not tied to per-host billing | — | New Relic — unified telemetry store, free tier available |
| Kubernetes-heavy, want auto-instrumentation with minimal setup | — | Dynatrace (OneAgent auto-instrumentation) or Metoro (eBPF-based, no manual instrumentation) |

Default recommendation for this skill's typical target (`architecture/scale_tiers.shared.md`'s Tier 1, small-team production): OpenObserve or SigNoz. Escalate to a paid platform only when a concrete requirement justifies it (compliance/support SLA, a specific debugging capability the self-hosted option lacks, or the operational cost of running it yourself exceeds the subscription) — same evidence-before-escalation reasoning as `architecture/complexity.shared.md`, applied to tooling rather than infrastructure.

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
