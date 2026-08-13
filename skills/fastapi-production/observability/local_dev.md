# Observability — Local Development

## Purpose
Provide useful diagnostics locally without requiring a full production telemetry platform.

## Rules
- Keep request IDs/correlation enabled.
- Prefer structured console logs.
- Console exporters are acceptable for tracing/metrics while developing instrumentation.
- Do not require a collector/backend locally unless the feature being developed depends on exporter or propagation behavior.
- Never print the full Settings object or secrets.

## Optional production-parity setup

```text
FastAPI
  ↓
OpenTelemetry SDK
  ↓
local Collector/backend
```

Use this when testing OTLP export, propagation, sampling, or collector configuration. [OpenObserve](https://github.com/openobserve/openobserve) is a good local backend for this: single ~40MB binary or Docker image, native OTLP ingestion for logs/metrics/traces on one port, no separate stack to run. Point the OTel SDK's OTLP exporter at it; no app code changes vs. any other OTLP backend.

## Tests
Verify:
- request ID appears in logs
- trace context propagates when enabled
- errors contain a correlation ID
- telemetry failures do not break the application
