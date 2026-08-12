# Rate Limiting — Shared

## Purpose

Define predictable, distributed-safe rate limiting policies to protect application infrastructure, prevent denial of service (DoS), and control access to sensitive business endpoints.

## Rules

- Apply rate limits to public endpoints, authentication paths (login, password reset), and expensive endpoints.
- Define explicit limit keys: IP address, authenticated user ID, tenant ID, or API key.
- Use shared Redis for multi-replica rate limiting state (process-local memory rate limiting is PARTIAL compatibility and does not protect across multiple gunicorn/uvicorn workers).
- Return HTTP `429 Too Many Requests` with a consistent `RATE_LIMITED` error contract and `Retry-After` header when quotas are exceeded.
- Use atomic Redis operations (Lua scripts or sliding window sorting via ZSET) to avoid race conditions during quota checks.

## Redis Sliding-Window Rate Limiter Pattern

```python
import time
from redis.asyncio import Redis
from fastapi import HTTPException, Request, status

class RedisRateLimiter:
    def __init__(self, redis: Redis, times: int = 10, seconds: int = 60):
        self.redis = redis
        self.times = times
        self.seconds = seconds

    async def check_rate_limit(self, key: str) -> None:
        now = time.time()
        clear_before = now - self.seconds
        redis_key = f"ratelimit:{key}"

        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(redis_key, 0, clear_before)
            pipe.zcard(redis_key)
            pipe.zadd(redis_key, {str(now): now})
            pipe.expire(redis_key, self.seconds)
            results = await pipe.execute()

        current_requests = results[1]
        if current_requests >= self.times:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(self.seconds)},
            )
```

## Sensitive Business Flow Limits

Rate limiting should be combined with business-specific controls for flows such as:
- `/api/v1/auth/login` (e.g. 5 attempts / minute per IP / username)
- `/api/v1/auth/password-reset` (e.g. 3 attempts / hour per email)
- `/api/v1/payments/charge` (e.g. 10 operations / minute per user)
- `/api/v1/ai/generate` (e.g. 20 calls / minute per user)

OWASP API6 treats unrestricted access to sensitive business flows as a distinct risk; a generic rate limiter alone may not preserve business constraints without tenant or action-specific keying.

## Forbidden

- process-local in-memory rate limiting as a production solution across multiple worker replicas
- trusting client-supplied `X-Forwarded-For` headers without an established reverse-proxy trust boundary
- GET/INCR/EXPIRE sequences without atomic pipeline/Lua execution
