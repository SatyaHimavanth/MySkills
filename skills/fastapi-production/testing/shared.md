# Testing — Shared

## Purpose

Make testing a design guardrail for the backend, not merely a collection of happy-path examples.

The test strategy must verify API contracts, business rules, security boundaries, database semantics, external dependency behavior, and production-sensitive concurrency.

## Test pyramid

Prefer the cheapest test that proves the requirement:

```text
             E2E / system
          contract / security
       API / integration tests
     service/domain tests
   unit tests / pure functions
```

Do not turn every test into an HTTP integration test. Do not unit-test infrastructure behavior with mocks when the actual semantics matter.

## Required test categories

Every production-grade backend should classify tests as appropriate:

- `unit`
- `api`
- `integration`
- `database`
- `security`
- `contract`
- `concurrency`
- `e2e`
- `slow`

Use pytest markers and register them explicitly. Pytest documents custom marker registration and recommends `--strict-markers` so spelling mistakes fail instead of becoming silent warnings. [Certain]

## pytest configuration

Recommended:

```toml
[tool.pytest.ini_options]
addopts = ["--strict-markers"]
markers = [
    "unit: fast isolated tests",
    "api: HTTP/API contract tests",
    "integration: tests requiring real or production-like dependencies",
    "database: tests requiring PostgreSQL/database semantics",
    "security: authentication/authorization/security tests",
    "contract: externally visible API contract tests",
    "concurrency: race/locking/idempotency tests",
    "e2e: full application workflow tests",
    "slow: tests that are intentionally expensive",
]
```

## uv workflow

Use uv for testing commands and test dependencies.

```bash
uv add --dev pytest pytest-cov anyio
uv run pytest
```

If a project uses a separate dependency group, put development/test tooling there according to the project's uv policy.

## Fixtures

Pytest fixtures should be:

- explicit
- composable
- deterministic
- scoped deliberately
- responsible for their own cleanup

Pytest documents fixture scopes and teardown as core mechanisms for scalable test suites. [Certain]

Prefer:

```text
session fixture → expensive shared infrastructure
function fixture → per-test state
```

Do not use session-scoped mutable application data merely for speed when tests can interfere with one another.

## Parametrization

Use `pytest.mark.parametrize` for a matrix of equivalent cases instead of copy/pasting tests. Pytest officially supports parametrizing both tests and fixtures. [Certain]

Example:

```python
@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("active", 200),
        ("disabled", 403),
    ],
)
def test_access(status, expected):
    ...
```

## Mocking policy

Mock at the boundary when the test is about application logic.

Do not mock a dependency when its actual semantics are the thing under test.

Examples:

```text
service validation → fake repository is fine
PostgreSQL isolation → use PostgreSQL
Redis atomic rate limiting → use Redis
HTTPX timeout behavior → use a controlled HTTP test server/mock transport
migration correctness → use PostgreSQL
```

A mock proves your code called the mock. It does not prove the real infrastructure behaves the same way.

## FastAPI dependency overrides

FastAPI provides `app.dependency_overrides` so tests can replace dependencies without running the original dependency or its sub-dependencies. [Certain]

Example:

```python
app.dependency_overrides[get_current_user] = get_test_user

try:
    ...
finally:
    app.dependency_overrides.clear()
```

Always clean up overrides.

Use overrides for:

- authenticated principals
- settings
- external providers
- expensive infrastructure when infrastructure semantics are not under test

## TestClient and lifespan

When lifespan behavior matters, use `TestClient` as a context manager:

```python
with TestClient(app) as client:
    response = client.get("/health")
```

FastAPI documents that the `with` block triggers lifespan startup and shutdown. [Certain]

## Async API tests

For async tests, use AnyIO plus HTTPX:

```python
@pytest.mark.anyio
async def test_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/api/v1/items")

    assert response.status_code == 200
```

FastAPI currently documents this exact `pytest.mark.anyio` + HTTPX `AsyncClient`/`ASGITransport` approach. [Certain]

Important: HTTPX `ASGITransport` does not trigger ASGI lifespan automatically. FastAPI documents using an ASGI lifespan manager when lifespan startup/shutdown must run in async tests. [Certain]

## Test isolation

Every test must leave the environment clean enough for the next test.

Avoid:

```text
test A creates global state
       ↓
test B assumes it exists
```

Prefer:

```text
fixture
  ↓
arrange
  ↓
test
  ↓
cleanup / rollback
```

## Deterministic tests

Avoid real timing sleeps where possible.

Use:

- injectable clocks
- fake time
- explicit polling with bounded deadlines
- deterministic fixtures

Do not write:

```python
time.sleep(5)
```

as the normal way to wait for application state.

## Test naming

Prefer behavior-oriented names:

```text
test_disabled_user_cannot_access_admin_route
test_duplicate_idempotency_key_returns_original_result
test_postgres_unique_constraint_maps_to_409
```

Avoid:

```text
test_user_1
test_new_feature
```

## Failure evidence

Tests should make failures diagnosable.

Prefer assertions that expose:

- HTTP status
- error code
- relevant response fields
- DB state
- job state
- correlation ID where useful

Avoid giant opaque snapshot assertions for critical API behavior.

## Coverage

Use coverage as a risk signal, not as proof of correctness.

`pytest-cov` provides coverage reporting and contexts, and supports distributed execution. [Certain]

Do not chase 100% line coverage while leaving important failure paths untested.

## Quality gate

Before declaring a feature complete, run the smallest meaningful set first:

```text
unit
  ↓
API/contract
  ↓
integration
  ↓
security/concurrency if affected
```

Then run the full suite when the change is ready.

## Forbidden patterns

- one global mutable test database for every test
- sharing one SQLAlchemy Session across tests
- using mocks to prove PostgreSQL/Redis behavior
- unregistered pytest markers
- ignored flaky tests without explanation
- sleeps instead of deterministic synchronization
- disabling security/authentication globally for API tests
- swallowing failing assertions

## Sources

- https://docs.pytest.org/en/stable/explanation/fixtures.html
- https://fastapi.tiangolo.com/tutorial/testing/

