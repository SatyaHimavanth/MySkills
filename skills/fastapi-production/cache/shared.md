# Caching — Shared

## Purpose

Use caching to reduce latency and load without violating freshness, authorization, tenancy, or correctness guarantees.

## Application cache vs HTTP cache

Keep these separate:

```text
application cache → service/backend state
HTTP cache         → client/CDN/proxy response caching
```

## Cache-aside

Default application pattern:

```text
cache GET
  ├─ hit → return
  └─ miss → source of truth → cache SET with TTL → return
```

## Cache keys

Include every dimension that changes the representation:

```text
tenant
user when relevant
resource
locale
permissions/representation
version
filter/sort inputs
```

Do not cache one tenant's private data under a global key.

## TTL and invalidation

Every cache entry must have an intentional:

- TTL
- invalidation strategy
- stale-data policy

For write-through or explicit invalidation, invalidate only after the authoritative source-of-truth transaction succeeds.

## Cache stampede

For hot expensive keys consider:

- request coalescing
- jittered TTLs
- stale-while-revalidate
- controlled distributed locking

Do not add a distributed lock unless the stampede is real and costly enough to justify it.

## Serialization

Cache stable DTO/Pydantic representations, not live ORM instances.

Version serialized representations when schema changes can invalidate old entries:

```text
user-summary:v2:{user_id}
```

## Failure policy

For reconstructable caches, a cache backend outage can usually fall back to the source of truth.

Do not apply that assumption to rate limiting or locks; those are separate semantics with their own failure policies.

## HTTP caching

Use `Cache-Control`, validators such as `ETag`, and `Vary` deliberately. Private/user-specific responses must not become reusable shared-cache responses accidentally.

## Metrics

Track:

- hit/miss ratio
- latency
- backend errors
- memory/evictions
- hot keys when observable

## Forbidden

- cache as source of truth without explicit architecture
- missing tenant/user dimensions in private cache keys
- no TTL/invalidation policy
- ORM objects in cache
- per-request Redis clients
- shared HTTP caching of private responses without explicit safety
