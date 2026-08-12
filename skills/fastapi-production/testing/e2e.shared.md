# End-to-End Testing — Shared

## Purpose

Verify complete business workflows across the real application boundaries.

## Use sparingly

E2E tests are slower and more operationally expensive than unit/API/integration tests.

Use them for workflows where several components must work together.

Examples:

```text
register → authenticate → create resource → process job → fetch result
upload → scan → store → enqueue → process → download
```

## Rules

- Use a dedicated test environment/data set.
- Do not depend on production data.
- Keep cleanup deterministic.
- Use stable test identities.
- Avoid coupling to implementation internals.
- Tag E2E tests as `e2e` and usually `slow`.

## External services

Use sandbox/test providers when the real provider behavior is part of the workflow.
Use fakes only when the external provider itself is not the subject of the test.
