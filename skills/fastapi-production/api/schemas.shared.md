# API Schemas — Shared

## Purpose

Make request and response payloads explicit, strictly validated, and decoupled from internal ORM models using Pydantic v2.

## Rules

- Use explicit Pydantic models for every request body and response payload boundary.
- Keep request models separate from response models (e.g. `UserCreateRequest` vs `UserResponse`).
- Use `ConfigDict(from_attributes=True)` on response models to allow direct serialization from SQLAlchemy ORM entities.
- Define field boundaries with `Field` constraints (`min_length`, `max_length`, `gt`, `le`, `pattern`).
- Keep OpenAPI examples realistic and secret-free.
- Document nullable fields (`str | None = None`) and PATCH updates (`model_dump(exclude_unset=True)`).

## Schema Inheritance & Organization Pattern

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Base shared fields
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=100, examples=["Jane Doe"])

# Request payload for creation
class UserCreateRequest(UserBase):
    password: str = Field(min_length=8, max_length=128, description="Plaintext password")

# Request payload for partial updates (PATCH)
class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, min_length=1, max_length=100)

# Public response payload
class UserResponse(UserBase):
    id: str = Field(examples=["usr_12345"])
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

## Route Usage & Partial Updates (PATCH)

```python
@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    # Exclude unset fields so omitted attributes are not wiped to None
    update_data = payload.model_dump(exclude_unset=True)
    updated_user = await service.update_user(user_id, update_data)
    return UserResponse.model_validate(updated_user)
```

## Contract Naming Convention

- `XCreateRequest`: Payload for `POST` operations
- `XUpdateRequest`: Payload for `PATCH` or `PUT` operations
- `XResponse`: Standard single entity payload
- `XListResponse`: Paginated or array collection response

## Forbidden

- returning SQLAlchemy ORM instances directly without a Pydantic `response_model`
- using `model_dump(exclude_none=True)` for PATCH endpoints (wipes fields that are intentionally set to `None`)
- exposing internal database columns (e.g. `hashed_password`, `internal_id`) in response models
