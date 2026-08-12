# Database Testing — Shared

## Purpose

Verify real PostgreSQL behavior without allowing tests to leak state into one another.

## Production parity

If production uses PostgreSQL, integration tests that depend on PostgreSQL behavior must use PostgreSQL.

SQLite may be used for narrow unit tests only when the tested behavior is portable and does not depend on PostgreSQL semantics.

Do not use SQLite to prove:

- PostgreSQL isolation behavior
- row locking
- PostgreSQL-specific SQL
- index behavior
- constraints with PostgreSQL-specific semantics
- migration safety
- connection-pool behavior

## Transaction isolation

A common strategy is:

```text
open connection
  ↓
begin external transaction
  ↓
create Session bound to connection
  ↓
test performs commits/flushes
  ↓
rollback external transaction
```

For more advanced suites, SQLAlchemy documents `join_transaction_mode="create_savepoint"` as particularly useful when integrating a Session into tests where an external transaction should remain unaffected. [Certain]

Example concept:

```python
connection = engine.connect()
transaction = connection.begin()

session = Session(
    bind=connection,
    join_transaction_mode="create_savepoint",
)

try:
    yield session
finally:
    session.close()
    transaction.rollback()
    connection.close()
```

The exact fixture must match the SQLAlchemy sync/async driver and database setup used by the project.

## SQLite warning

SQLAlchemy currently documents SAVEPOINT/transactional-testing caveats for SQLite, including Python 3.11's built-in SQLite driver behavior. Therefore do not blindly port a PostgreSQL transaction fixture to SQLite and assume equivalent isolation. [Certain]

## Migration tests

Every migration series should be validated against PostgreSQL.

Useful checks:

```bash
uv run alembic upgrade head
uv run alembic check
```

For destructive migrations, test upgrade from a representative pre-migration schema and validate important data invariants.

## Query tests

When testing a query optimization:

- populate representative data volume
- assert result correctness
- inspect the query count when relevant
- inspect query plans for performance-sensitive paths

Do not assert an exact query-plan text forever; assert the performance invariant that matters.

## Concurrency tests

Use real PostgreSQL for:

- row-lock behavior
- optimistic version conflicts
- deadlock/serialization retry behavior
- unique-constraint races
- idempotency races
- advisory locks

These cannot be reliably proven with a mock database.

## Sources

- https://docs.sqlalchemy.org/en/20/orm/session_api.html
- https://docs.sqlalchemy.org/en/20/orm/session_transaction.html

