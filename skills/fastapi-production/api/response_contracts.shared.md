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
    details: dict[str, object] | None = None

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
