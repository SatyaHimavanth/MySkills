# Local Fallbacks

## Purpose

Provide a safe path when production-shaped local infrastructure is unavailable.

## Compatibility levels

- `FULL`: sufficiently preserves required production semantics.
- `PARTIAL`: useful for development but cannot prove production semantics.
- `MOCK`: only for isolated tests/non-semantic code paths.

## Rules

- Explain the compatibility level before relying on a fallback that affects correctness.
- Prefer a real native/local service over a mock when production semantics matter.
- A Python implementation must share the same application interface as the production backend.
- Tests that depend on unsupported semantics must run against the real/closest production-compatible service in CI.

## Example

```text
Redis → RedisRateLimiter
No Redis → LocalMemoryRateLimiter
Compatibility → PARTIAL
```

The fallback must never be presented as proof that distributed Redis behavior works.

## Forbidden

- silent degradation
- unrelated stubs substituted for required infrastructure
