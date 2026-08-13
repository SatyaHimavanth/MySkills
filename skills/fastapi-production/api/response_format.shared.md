# Response Format — Shared

## Purpose

Keep API responses predictable for clients with a unified success and error envelope.

**This documents the enveloped-success convention.** `api/response_contracts.shared.md` documents the alternative bare-success convention (`response_model=UserResponse` directly, envelope only on errors). Pick one for the whole project — see that file for the reconciliation note. Do not apply both in the same API.

## Rules

- Use one stable success shape across the entire API.
- Use one stable error shape across the entire API.
- Include machine-readable error codes in error responses.
- Keep pagination metadata in a predictable, consistent location.
- Use Pydantic `response_model` so undocumented internal fields are never leaked.
- Return HTTP status codes that match the result.

## Standardized Response Envelope

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta: dict | None = None

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list[dict] | None = None

class ErrorResponse(BaseModel):
    success: bool = False
    data: None = None
    error: ErrorDetail
```

## Usage in Route Handlers

```python
@router.get("/users/{user_id}", response_model=SuccessResponse[UserResponse])
async def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    return SuccessResponse(data=UserResponse.model_validate(user))

@router.get("/users", response_model=SuccessResponse[PaginatedResponse[UserResponse]])
async def list_users(params: PageParams = Depends(), service: UserService = Depends(get_user_service)):
    items, total = await service.list_users(params)
    page_data = PaginatedResponse(items=items, total=total, page=params.page, size=params.size, pages=-(-total // params.size))
    return SuccessResponse(data=page_data)
```

## Response Categories

| Category | Status Code | Response Shape |
|:---|:---|:---|
| Success (single) | 200 | `SuccessResponse[T]` |
| Created | 201 | `SuccessResponse[T]` |
| Accepted (async job) | 202 | `SuccessResponse[JobAccepted]` |
| No Content | 204 | Empty body |
| Validation Error | 422 | `ErrorResponse` |
| Authentication Error | 401 | `ErrorResponse` + `WWW-Authenticate` header |
| Authorization Error | 403 | `ErrorResponse` |
| Not Found | 404 | `ErrorResponse` |
| Conflict | 409 | `ErrorResponse` |
| Rate Limited | 429 | `ErrorResponse` + `Retry-After` header |
| Server Error | 500 | `ErrorResponse` |

## Forbidden

- mixing envelope and non-envelope responses across different endpoints
- encoding HTTP errors as `200 OK` with an error body
- returning raw dictionaries without a `response_model`
