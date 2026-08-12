# Database: Local Development

## Purpose

Use a local database workflow that keeps PostgreSQL behavior close to production while allowing smaller resource settings and explicit infrastructure fallbacks.

## Rules

- Prefer PostgreSQL for normal development.
- Ask before using Docker/Podman when availability or permission is unknown.
- If containers are unavailable, prefer a native/local PostgreSQL installation or a permitted compatible service.
- SQLite requires an explicit user choice and a limitations warning.
- Keep SQLAlchemy models, Alembic migrations, transaction boundaries, and query patterns the same as production.
- Smaller connection pools are acceptable locally.
- Record the selected database/runtime in `.dev/environment.local.md`.

## Example

```env
APP_DATABASE__URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app
APP_DATABASE__POOL_SIZE=5
APP_DATABASE__MAX_OVERFLOW=5
```

## Verification

For DB semantics that affect production, run integration tests against PostgreSQL even when developers use another local fallback.

## Forbidden

- silently switching PostgreSQL to SQLite
- testing PostgreSQL-specific locking/transactions only against SQLite
- hard-coding developer-specific database paths
