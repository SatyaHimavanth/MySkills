# Error Handling — Production

## Purpose

Return stable safe error responses while retaining enough telemetry for operators to diagnose failures.

## Rules

- Never return stack traces, SQL, secrets, internal paths, or provider payloads.
- Use stable machine-readable error codes.
- Preserve required protocol headers such as `WWW-Authenticate` and `Retry-After`.
- Centralize exception translation.
- Emit structured error telemetry with request/trace correlation.
- Map database/provider failures to application semantics.

## 5xx behavior

```text
unexpected exception
  ↓
structured log + trace
  ↓
INTERNAL_ERROR
  ↓
500 response
```

## Forbidden

- leaking infrastructure details
- formatting different error envelopes per route
