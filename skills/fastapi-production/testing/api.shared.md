# API Testing — Shared

## Purpose

Test the public HTTP contract rather than implementation details.

## Every endpoint should have tests appropriate to its risk

At minimum consider:

- success case
- validation failure
- authentication failure
- authorization failure
- not-found/conflict behavior
- pagination/limits
- response schema
- relevant headers

## Contract assertions

Prefer:

```python
assert response.status_code == 201
body = response.json()
assert body["data"]["email"] == "user@example.com"
```

rather than asserting private service implementation calls.

## Error contract

Test:

```text
status_code
error.code
safe error message
required headers
```

Do not make clients depend on exact internal exception strings.

## OpenAPI contract

For important APIs, generate OpenAPI in CI and detect unintended contract changes.

Examples to inspect:

- path exists
- method exists
- request schema exists
- response schema exists
- security requirements exist
- deprecated routes remain marked

## Dependency overrides

Use FastAPI dependency overrides when the endpoint test needs a deterministic authenticated user or external provider. [Certain]

## API test separation

Do not make every API test require every external service.

Example:

```text
API validation test → app + fake dependencies
integration test    → app + real PostgreSQL/Redis
```

## Streaming tests

For streams verify:

- media type
- event/record format
- first bytes/events
- cancellation/disconnect
- resource cleanup

Do not buffer a huge production-sized response merely to assert the entire stream in memory.

## Sources

- https://fastapi.tiangolo.com/advanced/testing-dependencies/
- https://fastapi.tiangolo.com/advanced/async-tests/

