# Error Handling — Local Development

## Purpose

Make failures easy for developers to diagnose without changing the production API contract.

## Rules

- Keep the same HTTP error schema and error codes as production.
- Console logs may include stack traces and richer debugging context.
- API responses must remain safe and contract-compatible.
- Exercise validation, DB, auth, rate-limit, and external-dependency failure paths locally.
- Keep request IDs/correlation IDs enabled.

## Example

```text
HTTP response → safe ErrorResponse
Console log   → request_id + exception + traceback
```

## Forbidden

- returning stack traces from API responses
- using debug output as the public error contract
