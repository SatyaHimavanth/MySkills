# Deployment: Local Development

## Purpose

Run the same application contract locally while keeping infrastructure smaller and easier to operate.

## Rules

- Use `uv run` for project commands.
- Keep the same application entrypoint and router layout as production.
- Local `.env` may provide developer configuration; it is not a production configuration source.
- Prefer direct FastAPI development unless a proxy/load-balancer behavior is being tested.
- Use `--reload` only for development.
- Keep readiness/liveness routes available so deployment behavior can be exercised locally.

## Examples

```bash
uv run fastapi dev app/main.py
# or
uv run uvicorn app.main:app --reload
```

## Production-influence rule

Do not add local-only business logic to compensate for missing production infrastructure. Use adapters/configuration instead.

## Forbidden

- production secrets in local files
- local-only API contracts
- making process-local state part of the public behavior
