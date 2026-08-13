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
