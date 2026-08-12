# Database: Production

## Purpose

Define production PostgreSQL behavior, connection capacity, migration ownership, and failure handling.

## Rules

- PostgreSQL is required unless the project explicitly documents another production database.
- Size connection pools from worker/replica count and the database connection budget.
- Use `pool_pre_ping` where stale pooled connections are a realistic concern.
- Configure recycle/timeout behavior according to infrastructure limits.
- Handle connection failures and mid-transaction failures explicitly.
- Run Alembic migrations as a controlled deployment step rather than from every API worker.
- Keep database constraints and migration history authoritative for schema correctness.
- Do not let production schema drift from reviewed migrations.

## Capacity example

```text
4 replicas
5 pool connections
5 max overflow

Potential pool connections ≈ 4 × (5 + 5) = 40
```

Review that number against PostgreSQL's actual connection budget and other clients before deployment.

## Forbidden

- unlimited pool overflow
- per-request engine creation
- automatic migrations from every worker
- relying on local SQLite tests for PostgreSQL concurrency behavior
