# Error Handling — Shared

## Purpose

Translate domain and infrastructure failures into a unified, stable HTTP error contract while preventing internal leakage of stack traces, SQL syntax, or secrets.

## Rules

- Raise custom domain/application exceptions from service layers.
- Register centralized exception handlers in FastAPI (`app.add_exception_handler`).
- Return a standardized JSON error response body with machine-readable error codes.
- Map database errors (e.g. `IntegrityError`) and external provider failures to stable application error contracts.
- Never leak stack traces, raw SQL queries, internal directory paths, or credentials in response bodies.
- Preserve mandatory protocol headers (e.g. `WWW-Authenticate` for 401, `Retry-After` for 429).
- Log unexpected exceptions with request ID contextvars correlation.

## Standardized Error Response Model

```python
from pydantic import BaseModel
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list[dict] | None = None

class ErrorResponse(BaseModel):
    error: ErrorDetail

class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: list[dict] | None = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

class ResourceNotFoundError(AppError):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=f"{resource} with id '{identifier}' was not found",
            status_code=404,
        )

class DomainConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(code="CONFLICT", message=message, status_code=409)
```

## Centralized Handler Registration

```python
def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message, "details": exc.details}},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request payload",
                    "details": exc.errors(),
                }
            },
        )
```

## Client Error Code Standard

Clients should branch on `error.code`, never on human-readable error messages:

| Status Code | Error Code | Description |
|---|---|---|
| 400 | `BAD_REQUEST` | Malformed input payload or semantic violation |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication token |
| 403 | `FORBIDDEN` | Insufficient permissions for resource/scope |
| 404 | `RESOURCE_NOT_FOUND` | Target entity does not exist |
| 409 | `CONFLICT` | Concurrent edit, unique constraint, or state conflict |
| 422 | `VALIDATION_ERROR` | Request schema validation failure |
| 429 | `RATE_LIMITED` | Quota/rate limit exceeded |
| 500 | `INTERNAL_ERROR` | Unexpected server failure |

## Forbidden

- returning raw traceback strings in HTTP responses
- scattering `try ... except Exception:` blocks inside route handlers to format error JSON manually
- swallowing exceptions silently without logging
