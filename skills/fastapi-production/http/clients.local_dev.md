# Outbound HTTP — Local Development

## Purpose

Keep local external-service integration behavior compatible with production while allowing sandbox/test endpoints.

## Rules

- Reuse the same `httpx.AsyncClient` interface used in production.
- Configure provider URLs through Pydantic Settings.
- Keep TLS verification enabled unless a narrowly scoped developer certificate workflow requires an exception.
- Use explicit timeout categories even if values are shorter locally.
- Use sandbox/test providers when available.
- Use mocks only when the behavior under test does not depend on real provider semantics.
- Do not disable SSRF validation just because an endpoint is local.

## Example

```env
APP_EXTERNALS__PAYMENTS_BASE_URL=https://sandbox.example.com
```

## Forbidden

- creating an `AsyncClient` per request
- disabling certificate verification globally
- hard-coding provider URLs
