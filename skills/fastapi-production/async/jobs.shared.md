# Background Jobs — Shared

## Purpose

Separate small post-response work from durable asynchronous processing. FastAPI documents `BackgroundTasks` for work run after the response; it recommends larger queue/worker systems for heavy work or work spanning processes/servers.

## Decision table

| Work | Mechanism | Recommended Tools |
|---|---|---|
| tiny follow-up | `BackgroundTasks` | FastAPI built-in |
| durable / long-running | queue + worker | Taskiq, SAQ, Arq, Celery |
| CPU-heavy | separate process/worker | ProcessPoolExecutor, Celery, Taskiq |
| scheduled work | scheduler / cron | Taskiq-dependencies, APScheduler, SAQ cron |
| live progress | durable job + SSE/WebSocket/polling | Job DB table + Redis Pub/Sub + SSE |

## `BackgroundTasks`

Good for small, non-critical, loss-tolerant work:

```python
@router.post("/notifications", status_code=202)
async def notify(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_small_audit_record)
    return {"status": "accepted"}
```

Do not use it for payments, large file ingestion, AI model inference, large backfills, or work that must survive a process crash or restart.

## Durable Job Model

Persist job state in PostgreSQL:

```text
id, kind, status, attempt_count, available_at,
started_at, finished_at, last_error, payload/reference, timestamps
```

Use stable states:

```text
queued → running → succeeded
                 ↘ failed
queued/running → cancel_requested → cancelled
```

## Recommended Task Queues for FastAPI

- **Taskiq**: Modern async-first task manager with native FastAPI dependency injection support.
- **SAQ**: Lightweight, high-performance Redis-based queue using `asyncio`.
- **Arq**: Simple, lightweight Redis-based job queue built for `asyncio`.
- **Celery**: Battle-tested, multi-broker (RabbitMQ/Redis) queue for complex distributed workflows.

## Queue Abstraction

Business code should depend on an interface, not direct Redis/RabbitMQ SDK calls:

```python
from typing import Protocol
from uuid import UUID

class JobQueue(Protocol):
    async def enqueue(self, job_id: UUID, payload: dict) -> None: ...
```

Document the selected queue's delivery, ordering, retry, visibility, and durability semantics.

## DB + Queue Consistency

Do not assume these are atomic:

```text
DB commit + queue publish
```

When both must be reliable, prefer an outbox pattern — see `async/outbox.shared.md` for the concrete implementation and the polling-vs-CDC decision:

```text
DB transaction
 ├─ business mutation
 └─ outbox event
       ↓ commit
outbox publisher → queue → worker
```

`opentelemetry-instrumentation-httpx` auto-propagates `traceparent` on HTTP calls (see `http/clients.shared.md`) but not into queue/job payloads — inject it into the outbox event or job payload manually if trace continuity into workers matters.

## Retry Policy

Define max attempts, retryable errors, exponential backoff, jitter, timeout/lease, terminal failure, and optional DLQ behavior. Never retry every exception.

## Idempotency

Workers must tolerate duplicate delivery. Use DB uniqueness/state transitions/processed-event IDs.

## Cancellation

Prefer cooperative cancellation through durable state; do not promise immediate termination of arbitrary blocking work.

## Ordering

If ordering matters, define the ordering key and choose a queue/partitioning scheme that preserves it.

## Redis Streams

Redis Streams provide append-only entries and consumer groups with replay/coordination capabilities. They are a deliberate choice when those semantics are required, not a default queue merely because Redis is already present.

## Operations

Monitor queue depth, oldest-job age, throughput, latency, retries, failures, worker utilization, and DLQ growth.

## Forbidden

- durable work in `BackgroundTasks`
- job state stored only in process memory
- queue publish/DB commit with no consistency strategy
- infinite retries
- non-idempotent workers
- undocumented delivery semantics

## Sources

- https://fastapi.tiangolo.com/tutorial/background-tasks/
- https://redis.io/docs/latest/develop/data-types/streams/
