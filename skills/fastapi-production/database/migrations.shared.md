# Database Migrations — Shared

## Purpose

Make schema evolution reviewable, reproducible, and safe during rolling deployments using Alembic with async SQLAlchemy.

## Rules

- Use Alembic for schema migration history.
- Treat `--autogenerate` output as a candidate migration that must be manually reviewed.
- Run `alembic check` in CI to detect model/schema drift.
- Test migrations against PostgreSQL (not SQLite).
- Review destructive changes, locking risk, data-loss risk, and rolling-deployment compatibility.
- Prefer expand-and-contract for breaking schema changes.
- Separate large data backfills from normal request handling.
- Keep migration execution as a controlled deployment step rather than every API worker running it automatically.

## Alembic Async Setup

```python
# alembic/env.py
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from myapp.models import Base  # Import your DeclarativeBase
from myapp.config import get_settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = get_settings().db.url
    context.configure(url=str(url), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Workflow

```text
model change
 → alembic revision --autogenerate -m "add users table"
 → manual review of generated migration
 → PostgreSQL test DB validation
 → application tests
 → alembic check (CI)
 → controlled deployment (run migration before app starts)
```

## Expand and Contract

```text
expand schema (add new column with nullable/default)
 → deploy compatible application (writes to both old + new)
 → backfill/dual-write if needed
 → switch application to use new column exclusively
 → contract old column later (separate migration)
```

## Dangerous Examples

- dropping a column still used by an old replica
- making a populated column NOT NULL without a backfill plan
- rebuilding a large index without `CONCURRENTLY`
- running a multi-hour backfill inside an API request

## Verification Commands

```bash
uv run alembic current
uv run alembic heads
uv run alembic check
uv run alembic upgrade head --sql
```

## Source Basis

Alembic documentation: autogenerate produces candidate migrations that require review; `alembic check` detects new upgrade operations without generating a file.
