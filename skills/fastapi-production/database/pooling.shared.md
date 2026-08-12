# Database Connection Pooling — Shared

## Purpose

Control PostgreSQL connection reuse, capacity, stale-connection handling, and pool exhaustion across workers and replicas.

## Core rule

Pool sizing is a connection-budget decision, not a generic performance knob.

Approximate maximum application connections:

```text
workers × replicas × (pool_size + max_overflow)
```

Then account for migrations, admin tools, background workers, monitoring, and other services.

## Settings

Configure deliberately:

- `pool_size`
- `max_overflow`
- `pool_timeout`
- `pool_pre_ping`
- `pool_recycle` when the infrastructure/network has an idle-connection lifetime

Example:

```python
engine = create_async_engine(
    settings.database.url,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout_seconds,
    pool_pre_ping=True,
)
```

SQLAlchemy documents `pool_pre_ping` as a way to test pooled connections for liveness on checkout. Use it when long-lived pooled connections may become stale.

## Local development

A small pool is normally sufficient:

```text
pool_size = 5
max_overflow = 5
```

Do not copy production capacity values blindly into a developer laptop.

## Production sizing

Start with the PostgreSQL connection budget.

Example:

```text
DB max connections: 200
reserved/other clients: 40
application budget: 160
replicas: 4
```

That gives approximately 40 connections per replica before considering worker distribution. The actual per-process pool must be smaller if each replica runs multiple workers.

## Pool exhaustion

When the pool is exhausted:

- requests should fail within a bounded acquisition timeout
- the error should become a controlled `503`/dependency-unavailable path where appropriate
- operators should be able to observe pool pressure

Do not allow unbounded waiting for a connection.

## Connection lifecycle

Create engines/pools at application/resource scope, not per request.

Dispose them during application shutdown.

## Forbidden

- engine per request
- unlimited `max_overflow`
- ignoring worker/replica counts
- assuming `pool_size=20` is universally good
- silently increasing pool size to hide slow queries
