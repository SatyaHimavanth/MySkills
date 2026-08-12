# Lifespan — Production

## Purpose

Make resource initialization and shutdown compatible with multi-worker/multi-replica deployment.

## Rules

- Required resources must initialize before readiness.
- Shared clients/pools exist once per process and close on shutdown.
- Shutdown stops new work and releases resources deterministically.
- Lifespan must not run one-time database migrations; migrations belong to the deployment stage.
- A failed required resource must keep the instance unready.

## Multi-replica

Each replica owns its own process resources. Shared correctness belongs in PostgreSQL/Redis/queues/object storage rather than process memory.

## Readiness interaction

Lifespan completion is not identical to readiness. If a dependency can become unavailable after startup, readiness checks must reflect that operational state separately from one-time initialization.

## Shutdown behavior

Allow enough termination grace for short in-flight work and cleanup, but do not make graceful shutdown a substitute for durable job processing. Jobs that must survive process termination belong in the durable queue/worker model.
