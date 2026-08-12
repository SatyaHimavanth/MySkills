# Middleware — Local Development

## Purpose

Keep request lifecycle, security, and observability middleware behavior close to production while allowing more verbose development diagnostics.

## Rules

- Keep request IDs and error behavior consistent with production.
- Local logging/timing may be more verbose.
- CORS may include approved frontend development origins.
- Do not trust forwarded headers unless a local proxy is explicitly configured.
- Do not add middleware merely to mimic production infrastructure unless that behavior is being tested.
- Keep middleware stateless.

## Example

```text
local browser → FastAPI
```

A local proxy can be added for proxy/header/HTTPS testing, but it should be treated as a deliberate test environment.
