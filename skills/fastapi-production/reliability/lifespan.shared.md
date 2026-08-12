# Application Lifespan and Resource Ownership — Shared

## Purpose

Own application-wide resources explicitly and release them reliably. FastAPI recommends the `lifespan` async context manager for startup/shutdown resources such as database pools, Redis connections, and shared HTTP clients.

## Resource Ownership

Application-scoped resources include:

- SQLAlchemy engine
- Redis client/pool
- shared `httpx.AsyncClient`
- telemetry/exporter clients
- ML models or heavy singletons

Request-scoped resources include:

- `AsyncSession`
- authorization context
- request ID
- transaction

Do not mix scopes.

## Implementation Pattern

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    http_client = httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=3.0))
    db_engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db", pool_pre_ping=True)

    app.state.http = http_client
    app.state.db_engine = db_engine
    
    try:
        yield
    finally:
        # --- Shutdown ---
        await http_client.aclose()
        await db_engine.dispose()

app = FastAPI(lifespan=lifespan)
```

Use typed infrastructure containers or dependency wrappers when the project benefits from stronger typing.

## Accessing lifespan resources from dependencies

Resources stored on `app.state` during startup are retrieved through a small dependency function that reads `request.app.state`. This function **must** type-annotate its `request` parameter as FastAPI's `Request`:

```python
from fastapi import Depends, Request
from redis.asyncio import Redis

async def get_redis(request: Request) -> Redis:
    return request.app.state.redis

def get_cache(redis: Redis = Depends(get_redis)) -> Cache:
    return Cache(redis)
```

**If `request` is left untyped (`async def get_redis(request):`), FastAPI cannot recognize it as the injectable `Request` object and silently treats it as a required query parameter named `request` on every route that depends on it — directly or transitively.** This does not raise an error at startup or in the OpenAPI schema's absence; it appears as every affected route (including unrelated ones like login, if login is rate-limited through the same Redis dependency) returning `422 Unprocessable Entity` demanding a `request` query parameter, which is easy to misdiagnose as an auth or validation bug rather than a DI typing bug. Always check `/openapi.json` for an unexpected `request` query parameter on a route if you see this symptom.

This applies to any plain (non-route) dependency function that needs `Request`, `BackgroundTasks`, or other FastAPI-injectable types — not just resource accessors. The special-parameter recognition is based on FastAPI reading the type annotation; an unannotated or incorrectly annotated parameter degrades silently to "read this from the request" (query/body) instead of failing loudly.

## Initialization Order

```text
settings → telemetry → shared clients/pools → readiness → traffic
```

If a required dependency fails startup, fail startup immediately rather than silently accepting traffic in a broken state.

## Cleanup

Shutdown should stop producers, drain/cancel appropriate work, close clients, and dispose DB engines. Do not close shared clients from arbitrary route handlers.

## Sub-Applications

FastAPI documents that lifespan applies to the main application, not automatically to mounted sub-applications. Mounted resources need explicit ownership.

## Background Jobs

A durable worker creates its own DB session/clients. Never pass a request-scoped resource into a durable worker.

## Testing

Test startup and cleanup. Use `TestClient` as a context manager (`with TestClient(app) as client:`) when lifespan execution is part of the test.

## Forbidden

- engine/client creation per request
- `@app.on_event("startup")` / `@app.on_event("shutdown")` (deprecated; use `lifespan`)
- hidden startup failures
- closing shared resources from handlers
- putting request state into lifespan resources
- untyped `request` parameters in dependency functions that need `Request`, `BackgroundTasks`, or similar FastAPI-injectable types (silently becomes a query parameter instead of failing at startup)

## Sources

- https://fastapi.tiangolo.com/tutorial/lifespan/
