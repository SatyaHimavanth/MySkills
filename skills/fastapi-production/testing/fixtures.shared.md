# Test Fixtures — Shared

## Purpose

Define reusable, isolated pytest fixtures and test-resource ownership rules.

## Fixture ownership

Every fixture owns the setup and cleanup of the resource it creates.

Examples:

```text
settings fixture
DB engine fixture
DB session fixture
Redis fixture
HTTP client fixture
authenticated-user fixture
test-data factory
```

## Scope selection

Use the narrowest scope that avoids unnecessary setup cost.

```text
function → mutable test data
module   → expensive isolated resource when safe
session  → immutable/shared infrastructure only
```

## Database fixture

The fixture should provide an isolated transaction/session and guarantee cleanup.

## Auth fixture

Prefer factories:

```python
@pytest.fixture
def user_factory(db_session):
    def create_user(**overrides):
        ...
    return create_user
```

Do not create one permanent global user used by every test.

## Data factories

Factories should create valid minimal entities and allow targeted overrides.

Avoid huge fixtures that create unrelated domain state for every test.
