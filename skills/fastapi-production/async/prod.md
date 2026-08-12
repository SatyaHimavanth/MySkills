# Distributed Runtime — Production

## Rules

- Idempotency state is shared and durable.
- Long-running work uses durable job/queue infrastructure.
- Application-wide clients are owned by lifespan.
- Streaming events that cross replicas use shared infrastructure.
- Outbound HTTP calls have bounded timeouts/retries and idempotency-aware retry rules.

## Failure assumptions

Assume request retry, duplicate delivery, worker restart, dependency timeout, API instance termination, and lost streams. Durable state must remain correct after each event.

## Cross-replica verification

Validate the distributed contracts with multiple API instances/workers where applicable. Do not use one-process tests as proof of shared idempotency, queue correctness, or streaming event delivery.

## Operational requirements

Monitor job failures and backlog, idempotency conflicts, upstream timeouts/retries, and long-lived connection counts. Keep retry and timeout policies in typed settings so production changes do not require code edits.
