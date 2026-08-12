# Rate Limiting — Local Development

## Goal

Keep local rate-limit behavior compatible with the production interface while avoiding unnecessary infrastructure requirements for ordinary development.

## Rules

- Keep the same `RateLimiter` interface as production.
- An in-process implementation may be used for basic endpoint development.
- Mark in-process limiting as `PARTIAL` compatibility.
- Use real Redis locally when testing distributed quotas, concurrent requests, TTLs, or multi-worker behavior.
- Do not remove login/password-reset protection merely because development is local.
- Keep policy configuration visible even if local limits are relaxed.

## Local modes

```text
memory → fast development, PARTIAL
Redis  → production-parity behavior
```

## Discovery

Only require Redis when the selected local architecture needs it. Before using a local service, check the environment and container/native options.

## Forbidden

- claiming memory counters prove distributed production behavior
- silently changing limiter keys or algorithms between local and production
