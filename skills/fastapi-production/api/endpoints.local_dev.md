# Endpoint Management — Local Development

## Purpose
Keep local endpoint structure identical to the production API contract.

## Rules
- Use the same `/api/v1` prefixes and router boundaries as production.
- Use the same response/request models.
- Keep authentication/authorization behavior enabled unless the user explicitly requests a throwaway sandbox.
- Use development-only logging or test credentials through configuration, not route forks.
- Exercise deprecation and OpenAPI changes locally before release.

## Example
```text
/api/v1/users
/api/v1/documents
/api/v1/jobs
```

Do not create `/dev/users` merely because local infrastructure differs.

## Forbidden
- local-only endpoint shapes
- local-only response envelopes
- silently disabled authorization
