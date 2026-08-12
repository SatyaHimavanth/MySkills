# Testing — Local Development

## Purpose

Keep the feedback loop fast without lying about production behavior.

## Default commands

```bash
uv run pytest
uv run pytest -m "not slow"
uv run pytest -m unit
uv run pytest -m api
```

## Fast loop

Run:

```text
unit
API
small integration
```

before the full suite.

## Real services

Prefer local PostgreSQL and Redis when testing behavior that depends on their semantics.

If Docker/Podman is unavailable, use native local services or a documented PARTIAL fallback. Do not silently substitute SQLite/Memory for production-specific integration tests.

## Developer convenience

Acceptable:

- focused test selection
- console output
- smaller test datasets
- local fakes for unrelated external providers

Not acceptable:

- disabling authentication globally
- skipping DB integration coverage permanently
- replacing concurrency tests with unit mocks
