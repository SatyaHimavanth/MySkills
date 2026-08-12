# Transactions

## Purpose
Define business transaction boundaries, rollback, isolation, and locking behavior.

## Rules
- Repositories do not commit by default.
- The service/unit-of-work owns the transaction boundary.
- Use `flush()` when database-generated state is needed before commit.
- Roll back after failed transaction work before reusing the session.
- Use savepoints/nested transactions deliberately.
- Choose isolation level intentionally.
- Retry only known transient/serialization failures and only for operations safe to retry.
- Do not pretend a DB transaction atomically covers external HTTP, Redis, email, or object storage.

## Locking
Use `SELECT ... FOR UPDATE` only for real contention points. Keep lock ordering deterministic to reduce deadlocks.

## Savepoints

Use `begin_nested()` / savepoints when a sub-operation should be rolled back without losing the outer transaction. Do not use nested transactions as a substitute for a clear business transaction boundary.

## Isolation selection examples

- Normal CRUD: PostgreSQL Read Committed is often sufficient.
- Stable multi-read decision: consider Repeatable Read.
- Business invariant requiring serializable execution: use Serializable and implement bounded retry for serialization failures.

The correct choice depends on the invariant, not a generic "production" setting.
