# Database — Shared

## Purpose

Define the invariant database architecture used across local, test, staging, and production environments.

## Defaults

- PostgreSQL is the default database.
- SQLAlchemy is the application DB access layer.
- Alembic is the schema migration tool.
- API schemas are separate from ORM models.
- Sessions and transactions have explicit ownership.

## Application layering

```text
router
  ↓
service / unit of work
  ↓
repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

Routes should not contain large SQL/business rules. Repositories should not secretly create and commit their own sessions.

## Invariants

Use database constraints for data that must remain correct under concurrency:

- primary keys
- unique constraints
- foreign keys
- check constraints
- not-null constraints

Application validation improves client feedback but does not replace DB constraints.

## Transaction ownership

A transaction is a business unit of work. Choose a consistent service/unit-of-work strategy and do not scatter `commit()` across helper functions.

## Session ownership

Request-scoped FastAPI dependencies are a normal session-resource boundary. Durable background workers create their own sessions.

Read these detailed policies before implementation:

- `database/sessions.shared.md`
- `database/acid.shared.md`
- `database/transactions.shared.md`
- `database/concurrency.shared.md`
- `database/pooling.shared.md`
- `database/migrations.shared.md`
- `database/query_performance.shared.md` (plus `.local_dev.md`/`.prod.md`)
- `database/postgresql.shared.md`

## Environment rule

Local may use a smaller PostgreSQL topology, but the same SQLAlchemy/migration/query semantics should be used. SQLite requires explicit user selection and limitation disclosure.
