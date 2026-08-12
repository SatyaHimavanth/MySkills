# SQLAlchemy Session Lifecycle — Shared

## Purpose
Define ownership, setup, and lifetime of SQLAlchemy `AsyncSession` instances and SQLAlchemy 2.0 ORM conventions.

## Rules
- Session lifecycle is owned by an application/service/unit-of-work boundary, not by generic repositories.
- A FastAPI `yield` dependency is the standard request-scoped resource boundary.
- Repositories receive an active `AsyncSession` and do not create, commit, or close sessions independently.
- A session is not automatically the same thing as a business transaction; define transaction ownership explicitly.
- After a transaction failure, roll back before reusing or returning the session to the pool.
- Do not share one `AsyncSession` across concurrent asyncio tasks. SQLAlchemy documents one session per task for concurrent workloads.
- Do not pass a request-scoped session into durable background work; a background worker creates its own session.
- Avoid hidden lazy-loading database I/O during API serialization (use `selectinload`, `joinedload`, or `expire_on_commit=False`).

## SQLAlchemy 2.0 ORM Baseline

Use `DeclarativeBase`, `Mapped`, and `mapped_column`:

```python
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

## Async Engine & Session Setup

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/appdb",
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    echo=False,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevents implicit I/O during async Pydantic serialization
    autoflush=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

Repositories:
```python
from sqlalchemy import select

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
```

## Transaction Ownership
Choose one consistent model:

### Service-owned
```text
route → service → async with session.begin(): → repositories
```

### Unit-of-work-owned
```text
route → unit of work → service(s) → repositories → commit/rollback
```

Do not mix commit ownership randomly across repository methods.

## `expire_on_commit`
With async APIs, setting `expire_on_commit=False` in `async_sessionmaker` prevents SQLAlchemy from expiring *already-loaded* attributes after commit, avoiding `MissingGreenlet` or implicit async DB calls during Pydantic response serialization for ordinary columns.

**This does not cover server-generated columns on UPDATE.** `expire_on_commit=False` only stops the *whole object* from being expired; it does not stop SQLAlchemy from marking a specific attribute as "needs refresh" when that attribute has a `server_default` or `onupdate` value the ORM never received back from the database. If a mapped column uses `server_default=func.now()` or `onupdate=func.now()`, accessing that attribute after an INSERT/UPDATE will still trigger an implicit lazy load — which raises `MissingGreenlet` under the async driver, `expire_on_commit` setting notwithstanding.

Set `eager_defaults=True` on any mapped class that has `server_default`/`onupdate` columns you read back in the same request (e.g. returning the updated row in an API response). This makes SQLAlchemy use `RETURNING` to populate those columns immediately as part of the INSERT/UPDATE, instead of deferring and later lazy-loading them:

```python
class Task(Base):
    __tablename__ = "tasks"
    __mapper_args__ = {"eager_defaults": True}  # required: this table has onupdate=func.now()

    id: Mapped[str] = mapped_column(String, primary_key=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
```

Symptom if this is skipped: the first `UPDATE` (or, for some columns, `INSERT`) that touches the affected row and is then serialized into a response raises `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here`. This will not appear in local manual testing if you never read the column back immediately after a write — it surfaces as a 500 the first time a client does `PATCH` then reads the response body, so cover it explicitly in API tests, not just unit tests.

## Testing
Use isolated sessions/transactions or dedicated test databases (e.g. test containers or rollback fixtures). Do not share a mutable global session between tests.

## Forbidden

- `server_default`/`onupdate` columns read back in the same request without `eager_defaults=True` on that mapped class
- assuming `expire_on_commit=False` alone is sufficient to prevent `MissingGreenlet` on every column

## Source basis
SQLAlchemy 2.0 Async documentation: async session lifecycle, `DeclarativeBase`, `Mapped`, `mapped_column`, `async_sessionmaker`, and single task concurrency rules.
