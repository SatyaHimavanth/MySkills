# Caching — Production

## Goal

Provide shared, observable, failure-aware caching across production workers/replicas.

## Rules

- Use shared cache state when multiple instances must see the same cached representation.
- Define TTL and invalidation before deployment.
- Keep cache failure behavior explicit.
- Create Redis clients/pools at application resource scope and close them during shutdown.
- Monitor hit/miss rate, latency, memory/evictions, and backend errors.
- Do not use cache state as authoritative persistence unless the architecture explicitly chooses that model.

## Topology

```text
API replica 1 ─┐
API replica 2 ─┼→ shared cache
API replica 3 ─┘
```

## Failure policies

```text
cache → often fail-open to the source of truth
rate limiter → may require fail-closed
lock → explicit safety policy
```

Do not apply one Redis outage policy to every use case.
