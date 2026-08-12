# Observability — Shared

## Purpose

Make production behavior diagnosable through structured logs, metrics, traces, correlation, and safe telemetry using `structlog` and OpenTelemetry.

## Signals

```text
Logs    → events/context (structlog)
Metrics → aggregate behavior/saturation (Prometheus/OTel)
Traces  → request/dependency path (OpenTelemetry)
```

OpenTelemetry Python currently lists traces and metrics as stable and logs as development-status. Use OpenTelemetry for traces/metrics where appropriate, while keeping standard Python logging or `structlog` as the application logging foundation.

## Production `structlog` Implementation Pattern

```python
import sys
import structlog
from fastapi import FastAPI, Request
from starlette.types import ASGIApp, Receive, Scope, Send
import time

# Configure structlog for JSON logs in production, colored logs in dev
def setup_logging(debug: bool = False) -> None:
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    if debug:
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

# Middleware to bind request context variables to every log line
class StructlogContextMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()
        request_id = dict(scope.get("headers", [])).get(b"x-request-id", b"").decode() or "req_123"

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=scope.get("method"),
            path=scope.get("path"),
        )

        async def send_wrapper(message: dict) -> None:
            if message["type"] == "http.response.start":
                duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
                logger.info(
                    "http_request_completed",
                    status_code=message["status"],
                    duration_ms=duration_ms,
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)
```

## Request Context Fields

Make these available in structured logs:
- `request_id`
- `trace_id` (when OpenTelemetry tracing is active)
- `method`, `path`, `status_code`, `duration_ms`
- `environment`, `service_version`

## Sensitive Log Masking

Never log passwords, access tokens, refresh tokens, Authorization headers, API keys, private keys, session cookies, full request bodies, or sensitive uploaded content by default.

## Metrics

At minimum track request count, latency percentiles (p50, p95, p99), and error rates (`5xx`).

Avoid high-cardinality labels such as `request_id`, raw user IDs, or URLs containing resource IDs. Use route templates (e.g. `/api/v1/users/{id}`) instead of raw paths.

## Forbidden

- unstructured `print()` or string-formatting statements in production code
- high-cardinality label values in metrics
- logging authentication tokens, passwords, or PII
- telemetry export failure blocking API request threads
