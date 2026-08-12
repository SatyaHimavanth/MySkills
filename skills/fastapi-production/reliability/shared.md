# Reliability — Shared

## Purpose

Define failure, timeout, lifecycle, health, shutdown, retry, and dependency-degradation behavior that remains consistent across environments.

## Core rules

- Use FastAPI lifespan for application-scoped resource initialization/cleanup.
- Every external dependency needs an explicit timeout.
- Retry only known-transient failures and only when the operation is safe to repeat.
- Prefer bounded exponential backoff with jitter.
- Do not retry infinitely.
- Distinguish liveness from readiness.
- Decouple durable work from HTTP connection lifetime.
- Close resource clients/pools during shutdown.
- Make dependency failure behavior explicit: fail, degrade, cache, queue, or reject.

## Resource ownership

Application-scoped resources:

```text
DB engine/pool
Redis client/pool
HTTPX AsyncClient
telemetry exporters
```

Request-scoped resources:

```text
DB session
request-specific streams/files
```

Durable worker resources must be created inside the worker lifecycle.

## Timeouts before retries

A retry without a timeout can multiply outage impact. Configure timeout first, then retry policy, maximum attempts, and total retry budget.

## Health

```text
/liveness  → process health
/readiness → safe to receive traffic
```

Readiness may depend on required dependencies; liveness generally should not.

## Graceful shutdown

```text
stop new work
  ↓
drain/cancel active work
  ↓
close DB/Redis/HTTP clients
  ↓
stop workers
  ↓
exit
```

## Detailed policies

Read `reliability/lifespan.shared.md`, `reliability/degradation.shared.md`, and `reliability/circuit_breakers.shared.md` for resource lifecycle and failure-control rules.
