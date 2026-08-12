# OpenAPI and API Documentation

## Purpose
Treat the generated OpenAPI document as a reviewable API contract.

## Rules
- Give routers meaningful tags.
- Use stable operation IDs when generated clients matter.
- Add summaries/descriptions to externally consumed endpoints.
- Document request/response schemas and important errors.
- Add realistic examples without secrets or production data.
- Document OAuth2 scopes/security requirements.
- Mark deprecated operations explicitly.
- Keep generated OpenAPI deterministic enough for CI diffs.

## Example
```python
@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get a user",
    operation_id="get_user",
    responses={404: {"model": ErrorResponse}},
)
async def get_user(user_id: str) -> UserResponse:
    ...
```

## Contract review
CI should compare the generated schema when the API is externally consumed. Review additions, removals, required-field changes, enum changes, response/status changes, and security requirement changes.

Do not treat OpenAPI as a handwritten second source of truth when FastAPI can generate the contract from typed code.
