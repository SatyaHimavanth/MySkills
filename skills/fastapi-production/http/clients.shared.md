# Outbound HTTP Clients — Shared

## Purpose

Standardize external HTTP integrations around shared connection pools, bounded timeouts, safe retries, response validation, and observable failures. HTTPX documents pooled clients, default timeouts, and separate connect/read/write/pool timeout controls.

## Rules

- Use one application-scoped `httpx.AsyncClient` per distinct integration rather than a new client per request.
- Configure explicit connect/read/write/pool timeouts for every outbound integration. Never disable timeouts globally.
- Create long-lived clients during application lifespan (`@asynccontextmanager async def lifespan(app: FastAPI): ...`) and close them on shutdown.
- Validate downstream provider responses using Pydantic models with `model_validate_json`.
- Retry only known-transient errors (selected timeouts, 502/503/504) and only when the operation is retry-safe/idempotent.
- Use bounded exponential backoff plus jitter.
- Apply SSRF validation to user-controlled URLs before invoking the HTTP client.

## Shared Client

```python
client = httpx.AsyncClient(
    timeout=httpx.Timeout(10.0, connect=3.0, read=10.0, write=10.0, pool=2.0),
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
)
```

The numbers must be based on dependency quotas, latency, worker count, and DB/CPU connection budgets.

## Lifecycle

Create long-lived clients during application lifespan and close them during app shutdown. Store clients in `app.state` or inject via dependency wrappers.

## Timeouts

Configure connect/read/write/pool explicitly for important integrations. Never disable all timeouts globally.

## Retries and Backoff

Retry only known-transient errors and only when repeating the operation is safe. Use bounded exponential backoff plus jitter. Non-idempotent POST operations need idempotency before automatic retry.

## Circuit Breaker and Bulkhead

Use them for dependencies where repeated failure could exhaust app resources. They are explicit resilience controls, not default boilerplate.

## Response Validation

Validate provider responses with Pydantic models using `model_validate_json` for efficient parsing:

```python
class ProviderUser(BaseModel):
    id: str
    status: Literal["active", "inactive"]

response = await client.get(url)
response.raise_for_status()
user = ProviderUser.model_validate_json(response.content)
```

Never propagate arbitrary provider dictionaries directly into the domain layer.

## Error Translation

Map provider failures to stable application exceptions, for example timeout/503 → `DependencyUnavailable`, provider 429 → `UpstreamRateLimited`. Do not expose provider internals automatically.

## Security

User-controlled URLs require SSRF validation before the HTTP client is called. HTTPX is not itself an SSRF defense. Do not blindly follow redirects for security-sensitive URLs; validate redirect targets too.

Keep credentials in Settings and prefer authorization headers over query-string secrets. Do not manually copy incoming headers onto outgoing requests as a way to "forward" tracing — instrument the client with `opentelemetry-instrumentation-httpx` (`HTTPXClientInstrumentor().instrument()`) instead, which injects `traceparent` into every outbound call automatically. Manual header copying also leaks unrelated incoming headers downstream.

## Testing

Unit-test with a fake/mock transport (`httpx.MockTransport`). Integration-test critical provider behavior against a sandbox/test service when available. Cover success, timeout, connection failure, 4xx/5xx, malformed responses, retries, idempotency, and cancellation.

## Forbidden

- client-per-request at high volume
- infinite retries
- global timeout disablement
- retrying unsafe operations without idempotency
- treating provider JSON as trusted domain data
- blindly following user-controlled redirects
- logging API secrets

## Sources

- https://www.python-httpx.org/advanced/timeouts/
- https://www.python-httpx.org/advanced/resource-limits/
