# API Endpoints — Shared

## Purpose

Keep endpoint design, naming, route organization, and lifecycle management consistent using FastAPI `APIRouter` with domain-based module separation.

## Rules

- Use explicit API versioning via path prefix: `/api/v1/...`.
- Organize routes into domain routers using `APIRouter` with meaningful `prefix` and `tags`.
- Keep route handlers thin: validate input, call service, return response model.
- Apply authentication, authorization, and rate-limit dependencies explicitly per router or per endpoint.
- Define clear status-code contracts for success, validation, auth failure, conflicts, not-found, and dependency errors.

## Project Structure Pattern

```text
myapp/
├── main.py              # FastAPI app factory + lifespan + middleware
├── config.py            # Pydantic Settings
├── database.py          # Engine + async_sessionmaker + get_db_session
├── api/
│   ├── __init__.py
│   ├── deps.py          # Shared dependencies (get_current_user, get_db_session)
│   └── v1/
│       ├── __init__.py
│       ├── router.py    # Aggregates all v1 domain routers
│       ├── auth.py      # POST /login, /register, /refresh
│       ├── users.py     # GET/PATCH /users, GET /users/{id}
│       ├── projects.py  # CRUD /projects
│       └── tasks.py     # CRUD /projects/{id}/tasks
├── models/              # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py
│   ├── project.py
│   └── task.py
├── schemas/             # Pydantic request/response schemas
│   ├── __init__.py
│   ├── user.py
│   ├── project.py
│   └── task.py
├── services/            # Business logic layer
│   ├── __init__.py
│   ├── user_service.py
│   └── project_service.py
├── repositories/        # Database query layer
│   ├── __init__.py
│   ├── user_repo.py
│   └── project_repo.py
└── tests/
    ├── conftest.py
    ├── test_auth.py
    └── test_projects.py
```

## Router Organization Pattern

```python
from fastapi import APIRouter, Depends, status
from myapp.api.deps import get_current_user
from myapp.schemas.project import ProjectCreateRequest, ProjectResponse, ProjectListResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreateRequest,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    project = await service.create_project(payload, owner=current_user)
    return ProjectResponse.model_validate(project)

@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    params: PageParams = Depends(),
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
) -> ProjectListResponse:
    items, total = await service.list_projects(current_user, params)
    return ProjectListResponse(items=items, total=total, page=params.page, size=params.size)
```

## App Factory Pattern (`main.py`)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from myapp.api.v1.router import v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: create engine, redis, http clients
    yield
    # shutdown: dispose engine, close clients

def create_app() -> FastAPI:
    app = FastAPI(title="MyApp API", version="1.0.0", lifespan=lifespan)
    app.include_router(v1_router, prefix="/api/v1")
    return app

app = create_app()
```

## Endpoint Checklist

Every new endpoint should answer:
- Does an equivalent endpoint already exist?
- What is the request model? Response model?
- What status codes does it return (success and error)?
- Is the operation idempotent?
- Is pagination required?
- Is the operation long-running or stream-based?
- What auth/scope/role is required?

## Forbidden

- business logic directly inside route handler functions
- routes without explicit `response_model` declarations
- inconsistent URL naming (mixing `/get-users` with `/projects`)
