# Distributed Runtime — Local Development

## Purpose

Keep local infrastructure simple without changing API or correctness contracts.

## Rules

- Use PostgreSQL-backed idempotency for integration tests when duplicate safety matters.
- A local in-memory queue/cache is `PARTIAL` compatibility only.
- Use the same lifespan ownership model as production.
- Use the same shared HTTP client abstraction.
- Mock external providers in unit tests; use sandbox/test providers for integration tests when available.
- Use the same SSE/WebSocket/streaming protocol as production.

## Distributed testing

Run multiple workers/instances locally only when testing shared state, distributed rate limits, connection behavior, or cross-instance event delivery.

## Compatibility review

Local substitutes must be labeled FULL, PARTIAL, or MOCK. If a feature depends on cross-process delivery, durable queues, Redis atomicity, or provider-specific behavior, run a production-parity integration test against the real service or closest compatible service.

## Local verification commands

Use the repository's standard uv workflow, for example:

```bash
uv run pytest
uv run ruff check .
```

Do not add a local service merely because production uses it; first determine whether the current feature requires its semantics.
