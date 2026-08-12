# Rate Limiting — Production

## Goal

Protect the application and its dependencies from excessive traffic using policies that remain correct across workers and replicas.

## Rules

- Decide which controls belong in WAF/gateway infrastructure and which belong in FastAPI.
- Use shared state for quotas that must span workers/replicas.
- Redis is a common shared backend for application-level limits, but introduce it only for a concrete use case.
- Use atomic counter/expiry behavior.
- Configure keys and limits from typed settings.
- Return `429 Too Many Requests` with the stable error contract and `Retry-After` when applicable.
- Define the limiter-backend failure policy per security-sensitive endpoint.

## Key strategy

Choose deliberately among:

```text
IP
user ID
API key
tenant
user + endpoint
IP + endpoint
```

Authenticated endpoints often need identity-based limits in addition to coarse IP protection.

## Operational metrics

Track:

- rejected requests
- limiter latency
- backend errors/timeouts
- top limited endpoints
- suspicious bursts

Never use raw passwords, full API keys, or tokens as metric labels.
