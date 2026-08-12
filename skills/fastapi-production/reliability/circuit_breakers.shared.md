# Circuit Breakers — Shared

## Purpose

Define when and how to isolate repeatedly failing outbound dependencies.

## Use only for failure amplification

Circuit breakers are appropriate when a dependency failure can cause:

- request pileups
- connection-pool exhaustion
- worker starvation
- cascading retries
- cascading failures across services

Do not add a breaker merely because a library offers one.

## State machine

```text
CLOSED
  │ failures over threshold
  ▼
OPEN
  │ cool-down elapsed
  ▼
HALF-OPEN
  ├── successful probes → CLOSED
  └── failed probe      → OPEN
```

## Configuration

Use typed settings for:

- failure threshold/window
- open duration
- half-open probe count
- minimum request volume
- excluded status codes

Do not hard-code values in business logic.

## Failure classification

Usually count:

- connect timeout
- read timeout
- connection refusal
- dependency `5xx`
- explicitly classified transient failures

Usually do not count:

- caller `4xx`
- validation failures
- authentication failures
- resource `404`

## Interaction with retries

Prefer:

```text
circuit breaker
      ↓
small bounded retry policy
      ↓
timeout
```

or another explicitly reviewed order consistent with the selected library. Avoid nested independent retry systems at both the HTTP client and service layer.

## Metrics

Expose:

- current state
- opens
- half-open probes
- rejected calls
- dependency failures
- latency

Do not expose high-cardinality request data as labels.

## Testing

Test:

- transition to OPEN
- cool-down
- half-open success
- half-open failure
- excluded failures
- concurrent calls while open
- process restart behavior

If the breaker state must survive process restarts or be coordinated across replicas, explicitly decide whether it belongs in shared infrastructure. Many applications can safely keep the breaker local to each instance because it protects that instance's resources; do not introduce distributed breaker state without a clear requirement.
