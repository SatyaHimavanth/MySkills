# Caching — Local Development

## Goal

Provide a fast local cache path without teaching the application incorrect multi-worker assumptions.

## Rules

- Keep the same `CacheBackend` interface as production.
- In-memory cache is `PARTIAL` compatibility.
- Use real Redis locally for distributed-cache/rate-limit/lock testing.
- Keep cache keys, serialization, TTL, and invalidation logic the same as production.

## Example

```env
APP_CACHE__BACKEND=memory
APP_CACHE__DEFAULT_TTL_SECONDS=60
```

Redis parity:

```env
APP_CACHE__BACKEND=redis
APP_REDIS__URL=redis://localhost:6379/0
```

## Forbidden

- process-local cache for a feature that requires shared state
- changing key semantics only for local development
