# Middleware — Production

## Purpose

Keep middleware secure, predictable, and efficient under multiple workers/replicas.

## Rules

- Keep middleware stateless.
- Preserve request IDs and tracing context.
- Trust forwarded headers only from known proxies/hops.
- Keep CORS and security-header policy explicit.
- Avoid blocking work in middleware.
- Review middleware order whenever adding/removing middleware because ordering changes observable security and response behavior.
- Prefer pure ASGI middleware when `contextvars` propagation matters.

## Performance

Middleware runs on every request. Keep it bounded and avoid database/network work unless the cross-cutting requirement genuinely requires it.

## Forbidden

- global mutable middleware state
- arbitrary client-supplied forwarded headers
