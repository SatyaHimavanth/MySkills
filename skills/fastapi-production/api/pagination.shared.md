# Pagination — Shared

## Purpose

Prevent uncontrolled result sizes, prevent memory exhaustion, and standardize list endpoint contracts using typed Pydantic request/response wrappers and efficient database queries.

## Rules

- Every list endpoint must define its pagination strategy (offset or cursor).
- Enforce a mandatory maximum page size (e.g. `limit <= 100`, default `limit = 20`).
- Use offset pagination for small, searchable, user-facing administration views.
- Use cursor-based pagination for high-volume, real-time, or continuously updated feeds to avoid offset degradation and skipped/duplicated items.
- Order paginated queries deterministically by adding primary keys to the sort key (`ORDER BY created_at DESC, id DESC`).

## Offset Pagination Pattern

```python
from typing import Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class PageParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    size: int = Field(default=20, ge=1, le=100, description="Page size limit")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(from_attributes=True)

async def paginate_offset(
    session: AsyncSession,
    query,
    params: PageParams,
) -> tuple[list, int]:
    # Count total items
    count_stmt = select(func.count()).select_from(query.subquery())
    total = (await session.execute(count_stmt)).scalar_one()

    # Fetch page
    page_stmt = query.offset(params.offset).limit(params.size)
    items = (await session.execute(page_stmt)).scalars().all()

    return list(items), total
```

## Cursor-Based Pagination Pattern

```python
import base64
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class CursorParams(BaseModel):
    cursor: str | None = None
    limit: int = Field(default=20, ge=1, le=100)

class CursorPaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
    has_more: bool

def encode_cursor(created_at: str, item_id: str) -> str:
    raw = f"{created_at}|{item_id}"
    return base64.b64encode(raw.encode()).decode()

def decode_cursor(cursor_str: str) -> tuple[str, str]:
    decoded = base64.b64decode(cursor_str.encode()).decode()
    created_at, item_id = decoded.split("|")
    return created_at, item_id
```

## Forbidden

- unbounded list endpoints without default limits
- dynamic client-supplied limit without enforcing `le=100` ceiling
- non-deterministic `ORDER BY` clauses (e.g. sorting only by non-unique fields like `created_at`)
