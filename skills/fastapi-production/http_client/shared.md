# Outbound HTTP Clients — Shared Policy

## Purpose

Provide detailed policy and rules for outbound HTTP client management, pooled connections, bounded timeouts, retries, and response validation across production and local FastAPI services.

## Rules

- Use a single application-scoped `httpx.AsyncClient` instance per integration rather than instantiating a client per-request.
- Explicitly configure connect, read, write, and pool timeouts on all outbound HTTP clients.
- Create HTTP clients inside FastAPI lifespan handlers and ensure proper cleanup during application shutdown.
- Validate downstream provider responses using Pydantic `model_validate_json` for response validation.
- Implement idempotency checks before retrying non-idempotent HTTP requests.
- Handle provider errors with bounded retries and exponential backoff plus jitter.
- Apply strict SSRF validation to user-controlled URLs before calling outbound HTTP services.

## Implementation Guidelines

FastAPI applications making outbound HTTP calls should manage `httpx.AsyncClient` inside the lifespan context manager:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, connect=3.0, read=10.0, write=10.0, pool=2.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )
    yield
    await app.state.http_client.aclose()
```

Refer to `http/clients.shared.md` for full implementation patterns, connection pooling details, circuit breaker controls, and security recommendations.
