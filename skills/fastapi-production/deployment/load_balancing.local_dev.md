# Load Balancing — Local Development

## Goal

Keep normal development simple while ensuring application code remains compatible with future load balancing.

## Normal local topology

```text
client → FastAPI → PostgreSQL/shared services
```

Do not require a real load balancer for ordinary local work.

## Simulate production only when testing

Multiple workers/instances are useful for validating:

- shared state
- rate limits
- readiness
- proxy headers
- concurrency
- long-lived connections

## Forbidden

- coding against one-process-only state
- adding a reverse proxy solely for appearance
