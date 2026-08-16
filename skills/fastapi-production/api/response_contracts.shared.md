# API Response Contracts

## Purpose
Define stable, typed HTTP response contracts that are independent of internal ORM/domain models.

## Rules
- Normal JSON endpoints should declare a Pydantic `response_model`.
- Keep request schemas and response schemas separate when their contracts differ.
- Do not expose SQLAlchemy models directly as the public API contract.
- HTTP status codes are part of the API contract.
- Use one documented error shape and stable machine-readable error codes.
- Do not force binary, file, SSE, or WebSocket responses into a JSON envelope.

## Success envelope: pick one project-wide convention

This file's example returns the response model directly (`response_model=UserResponse`, bare body). `api/response_format.shared.md` documents an alternative `SuccessResponse[T]` wrapper (`{success, data, meta}`) for projects that want one shape for both success and error bodies. **These are two valid, mutually exclusive conventions, not two independent mandates** — a project must pick exactly one and apply it to every endpoint. Mixing bare and enveloped success responses across endpoints in the same API is the actual "Forbidden" case both files warn against. If your project already has `errors/shared.md`'s bare `{"error": {...}}` error handlers wired up (no `success`/`data` wrapper), use the bare-success convention shown below for consistency, since that's what those exception handlers already produce.

## Example
```python
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID) -> UserResponse:
    ...
```

FastAPI's `response_model` participates in validation, serialization/filtering, and OpenAPI generation. See the current FastAPI response-model documentation.

## Error contract
```python
class ErrorDetail(BaseModel):
    code: str
    message: str
    # FastAPI's RequestValidationError.errors() returns list[dict[str, Any]] — keep this a list,
    # not a single dict, or populating it from validation errors will fail type validation.
    details: list[dict] | None = None

class ErrorResponse(BaseModel):
    success: bool = False
    data: None = None
    error: ErrorDetail
    meta: dict[str, object] | None = None
```

## Rules for compatibility
- Additive response fields may be backward compatible only if clients tolerate them.
- Removing or renaming fields, changing nullability, status codes, or error shapes is a breaking change.
- Breaking changes require an explicit API version or migration plan.

## Custom exception-handler status codes do not appear in the OpenAPI schema by default

**Verified end-to-end**: a `@app.exception_handler(DomainError)` that returns `409`/`401`/`403`/`429` for business errors (email already registered, invalid credentials, rate limited, etc.) makes the *runtime* behavior correct — the actual HTTP response is right — but FastAPI's OpenAPI generator only documents the status codes a route declares (its `response_model`'s implicit `200`/`201` and anything in `responses=`). A global exception handler is invisible to schema generation. Confirmed by inspecting a live `/openapi.json`: a route raising `EmailAlreadyRegisteredError` (409) and protected by rate limiting (429) showed only `201` and `422` in its schema until those were added explicitly.

This matters beyond documentation completeness: `frontend-api-client`'s entire premise is generating a typed client and error types *from this schema*, so contract drift becomes a build error. A status code missing from the schema is a status code the generated client's error type doesn't know exists — the frontend gets no compile-time signal that a 409 or 429 can happen, even though the backend correctly returns one at runtime.

Declare every non-2xx status code a route can actually return via `responses=`, pointing at your project's `ErrorResponse` model:

```python
from fastapi import status

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": ErrorResponse, "description": "Email already registered."},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ErrorResponse},
    },
)
async def register_user(...) -> UserResponse:
    ...
```

For status codes shared across most routes (e.g. `429` on every rate-limited endpoint, `401` on every authenticated one), set them once via `APIRouter(..., responses={...})` or `include_router(..., responses={...})` instead of repeating them on every route; add route-specific codes (like a `409` unique to registration) on top of that shared set.

### Forbidden
- relying on a global `@app.exception_handler` alone to "document" an error response — it fixes runtime behavior only, not the schema
- assuming a codegen tool's output is complete because it ran without errors — a missing status code produces a *valid but incomplete* schema, not a codegen failure, so nothing will flag it

