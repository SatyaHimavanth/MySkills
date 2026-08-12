# Architecture — Shared

## Purpose

Keep backend structure predictable, layered, and resistant to architectural drift during AI-assisted development.

## Rules

- Use a strict layered design: **API → Service → Repository → Database/External**.
- Keep FastAPI route handlers thin (validate → call service → return response model).
- Keep business logic in service classes, never in route handlers or repositories.
- Keep API schemas (Pydantic) separate from ORM models (SQLAlchemy).
- Use FastAPI dependency injection for cross-cutting concerns (settings, DB sessions, auth context, services).
- Treat production constraints as design inputs even during local development.

## Layer Responsibilities

```text
┌──────────────────────────────────────────────────────┐
│  API Layer (FastAPI Routes)                          │
│  - HTTP input validation (Pydantic request models)   │
│  - Authentication / Authorization dependencies       │
│  - Call service layer                                │
│  - Return Pydantic response models                   │
├──────────────────────────────────────────────────────┤
│  Service Layer (Business Logic)                      │
│  - Orchestrates business rules                       │
│  - Calls repository methods                          │
│  - Owns transaction boundaries (commit/rollback)     │
│  - Raises domain exceptions (not HTTPException)      │
├──────────────────────────────────────────────────────┤
│  Repository Layer (Data Access)                      │
│  - Encapsulates SQLAlchemy queries                   │
│  - Receives AsyncSession (does not create/commit)    │
│  - Returns ORM model instances                       │
├──────────────────────────────────────────────────────┤
│  Models Layer (SQLAlchemy ORM + Pydantic Schemas)    │
│  - ORM models define database table structure        │
│  - Pydantic schemas define API contracts             │
│  - These are SEPARATE — never expose ORM as API      │
└──────────────────────────────────────────────────────┘
```

## Dependency Injection Pattern

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from myapp.database import get_db_session
from myapp.repositories.user_repo import UserRepository
from myapp.services.user_service import UserService

def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)
```

## Forbidden

- importing SQLAlchemy `Session` inside route handler functions
- services raising `HTTPException` (they should raise domain exceptions)
- repositories calling `session.commit()` (services own transactions)
- ORM model instances returned directly as API responses
