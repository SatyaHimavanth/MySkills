# Outbound HTTP — Production

## Purpose

Make downstream calls bounded, pooled, observable, secure, and retry-safe.

## Rules

- Use a shared pooled `httpx.AsyncClient` with explicit lifecycle.
- Set connect/read/write/pool timeouts deliberately.
- Verify TLS certificates.
- Bound connection counts and downstream concurrency.
- Retry only known transient and idempotent-safe failures.
- Honor provider retry guidance and `Retry-After` where applicable.
- Validate response payloads with typed schemas when the response is used as trusted application data.
- Protect user-controlled destinations with SSRF controls.
- Emit downstream latency/error telemetry.

## Forbidden

- unbounded retries
- disabling TLS verification
- trusting arbitrary provider JSON without validation
