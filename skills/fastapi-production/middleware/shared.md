# Middleware — Shared

## Purpose

Define which concerns belong in ASGI middleware versus FastAPI dependencies/services, explain Starlette `BaseHTTPMiddleware` vs pure ASGI middleware caveats, and make middleware ordering predictable.

## Use middleware for cross-cutting request/response concerns

Good candidates:

- request/correlation ID injection
- timing and performance metrics
- trusted proxy integration (`ProxyHeadersMiddleware`)
- CORS (`CORSMiddleware`)
- security headers
- request-wide telemetry / logging context

Do not put business authorization, DB transactions, or resource-specific logic into global middleware merely because middleware runs on every request.

## `BaseHTTPMiddleware` vs Pure ASGI Middleware

Starlette's `BaseHTTPMiddleware` is convenient but has known architectural caveats in production async applications:

1. **Contextvar propagation**: `BaseHTTPMiddleware` runs the request handler in a separate `asyncio` task, which can prevent `contextvars` mutations (e.g., setting a request ID in context) from being inherited by child tasks or downstream handlers.
2. **Streaming & performance**: `BaseHTTPMiddleware` wraps response bodies in an async iterator, adding overhead for streaming responses.

**Recommendation**:
- For simple header/timing middleware, `BaseHTTPMiddleware` is acceptable.
- When `contextvars` (e.g., request ID tracking across async calls / structured logging) or high-throughput response streaming are needed, use a **pure ASGI middleware**:

```python
from starlette.types import ASGIApp, Receive, Scope, Send
import contextvars
import uuid

request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")

class RequestIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Extract the incoming request ID from an upstream proxy if present, else generate one.
        headers = dict(scope.get("headers", []))
        request_id = headers.get(b"x-request-id", b"").decode() or str(uuid.uuid4())
        token = request_id_ctx.set(request_id)
        
        try:
            await self.app(scope, receive, send)
        finally:
            request_id_ctx.reset(token)
```

## Ordering

Review order deliberately. Typical concerns include:

```text
proxy/trust boundary
  ↓
request ID / tracing
  ↓
CORS
  ↓
security headers
  ↓
rate limiting where implemented globally
  ↓
FastAPI routing/dependencies
```

The exact ordering depends on the project and threat model.

## Dependency vs middleware

Use a dependency when the concern is endpoint/resource-specific:

- authentication
- authorization
- DB session
- service injection

Use middleware when every request/response needs the concern.

## Resource ownership

Middleware must not retain request-scoped DB/HTTP clients or mutable state beyond the request lifecycle unless explicitly designed for that scope.
