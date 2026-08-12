# Database Migrations — Local Development

## Purpose
Use the same Alembic history locally that CI and production use.

## Rules
- PostgreSQL is the default local target.
- Apply migrations with `uv run alembic upgrade head`.
- Review generated migrations before committing.
- Use `uv run alembic check` before changes are submitted.
- Use disposable PostgreSQL databases for destructive migration experiments when practical.
- SQLite may be used only when explicitly requested; it is not sufficient to validate PostgreSQL-specific migration behavior.

## Workflow
```bash
uv run alembic upgrade head
uv run alembic check
uv run pytest
```
