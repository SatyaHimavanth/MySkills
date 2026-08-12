# Graceful Degradation and Failure Isolation — Shared

## Purpose

Keep a partially failing FastAPI service useful instead of allowing one dependency or overload condition to cascade into a total outage.

Google Cloud's reliability guidance describes graceful degradation as continuing to provide service, potentially with reduced performance or accuracy, during overload or dependency failure. It specifically discusses throttling, dropping excess work early, and handling partial errors. [Certain] See the official reliability guidance. 

## Core rule

For every non-core dependency, decide explicitly:

```text
dependency fails
    ↓
full failure / degraded result / cached result / queued work / reject early
```

Do not let the default exception path decide the user experience accidentally.

## Dependency criticality

Classify dependencies:

### Critical

The request cannot be correct without the dependency.

Examples:

- primary PostgreSQL for a write that must persist
- authorization source when authorization cannot safely be inferred

Failure should normally produce a controlled `503` or equivalent safe error.

### Degradable

The core response can continue without the dependency.

Examples:

- cache
- optional enrichment API
- telemetry exporter
- recommendation service

The application can return a degraded result.

### Asynchronous

The dependency can be replaced by durable background work.

Examples:

- report generation
- email delivery
- indexing
- document processing

## Bulkheads

Do not allow one expensive dependency to consume every application resource.

Use bounded:

- HTTP connection pools
- database pools
- worker concurrency
- queue concurrency
- semaphore limits
- upload sizes

Example:

```python
external_api_limit = asyncio.Semaphore(20)

async with external_api_limit:
    return await client.get(...)
```

The exact limit belongs in typed configuration and must be load-tested rather than copied blindly.

## Timeouts first

A circuit breaker is not a substitute for a timeout.

The sequence should usually be:

```text
bounded timeout
     ↓
bounded retry where appropriate
     ↓
circuit-breaker policy where justified
     ↓
degraded/fallback response
```

## Circuit breakers

Use a circuit breaker only when repeated dependency failures can create cascading load.

A typical model:

```text
closed
  ↓ repeated failures
open
  ↓ cool-down
half-open
  ↓ success → closed
  ↓ failure → open
```

A breaker should have explicit:

- failure criteria
- timeout
- open duration
- half-open probe policy
- maximum concurrent probes
- excluded errors
- metrics

Do not count normal client errors such as `404` as dependency outages unless the policy explicitly says so.

## Retries and load amplification

Retries can multiply load during an outage.

For example:

```text
100 requests
 × 3 retries
 = up to 400 dependency attempts
```

Use retries only for known transient errors and bound attempts/backoff.

Do not retry:

- validation errors
- authorization failures
- deterministic `404`
- non-idempotent operations without idempotency protection

## Fallbacks

Every fallback must define its compatibility and freshness semantics.

Examples:

```text
Redis unavailable
    → DB/source of truth

Recommendation API unavailable
    → core result without recommendations

Telemetry unavailable
    → continue serving requests

Queue unavailable
    → reject/mark pending based on job durability policy
```

Never fabricate successful results for correctness-critical data.

## Load shedding

Protect the system by rejecting excess work early.

Examples:

- `429` for policy limits
- `503` for temporarily unavailable capacity
- maximum queue depth
- concurrency semaphore
- maximum request/upload size

Rejecting a bounded amount of work is preferable to allowing every instance to become unresponsive.

## Error budget interaction

Graceful degradation should be reflected in SLOs.

A response that is technically `200` but missing a contractual critical result may need to count as unsuccessful depending on the service's user-visible SLI.

## Forbidden patterns

- infinite retries
- retrying without timeouts
- circuit breaker around every function
- fallback that returns fabricated authoritative data
- unbounded concurrency
- using cache as an invisible source of truth
- letting one downstream dependency consume the entire process pool
