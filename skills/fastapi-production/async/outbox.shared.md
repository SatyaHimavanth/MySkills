# Transactional Outbox — Shared

## Purpose
Solve the dual-write problem: a DB commit succeeds, then the process crashes/network fails before the corresponding event/job is published — the write is silently lost from downstream consumers. `async/jobs.shared.md`'s "DB + Queue Consistency" section sketches this pattern in outline; this file adds the concrete implementation, the polling-vs-CDC decision, and trace propagation.

Verified directly: committed a business write + outbox row in one transaction, then simulated a hard crash with zero publish attempt (no relay ran at all). A completely fresh process/connection afterward — with no in-memory state from the "crashed" one — still found the event sitting in the table and correctly delivered it. The durability came entirely from the DB transaction, not from anything the original process remembered.

## Pattern
Write the business row and an outbox row in the **same DB transaction** — atomic by construction, no separate publish step that can fail independently.

```python
async def create_order(self, ...):
    order = await self.repo.create(...)
    await self.session.add(OutboxEvent(
        aggregate_type="order", aggregate_id=order.id,
        event_type="order.created", payload=order_dto,
    ))
    await self.session.commit()  # order + event: both or neither
```

A separate relay process reads unpublished outbox rows and publishes them, marking them sent (or deleting them) after confirmed delivery — never before.

## Start with polling, not CDC
Default: a periodic job (via `async/jobs.shared.md`'s worker pattern) polls, publishes, marks sent:
```sql
SELECT id, event_type, payload FROM outbox_events
WHERE published_at IS NULL ORDER BY created_at LIMIT 10 FOR UPDATE SKIP LOCKED;
```
`FOR UPDATE SKIP LOCKED` is required, not optional, the moment more than one relay instance runs (the normal way to make the relay itself highly available). Verified: two relay workers polling the same unpublished rows concurrently, without this clause, would both select and publish the same events; with it, confirmed zero duplicates across concurrent workers — each row goes to exactly one worker, the other silently skips locked rows and picks up whatever's left. Simple, debuggable, no new infrastructure.

Move to CDC (Debezium reading the PostgreSQL WAL via logical replication) only once polling latency or DB load from polling actually becomes a measured problem — CDC adds real operational cost (replication slot management, connector monitoring, WAL growth if the slot falls behind) that isn't justified pre-emptively.

## Trace context
If downstream consumers need distributed tracing continuity, inject `traceparent` into the outbox payload at write time — it does not propagate automatically into a queue/table the way `http/clients.shared.md`'s HTTP calls do.

## Forbidden
- publishing directly to a broker/queue in the same code path as the DB write, with no outbox table backstop
- deleting/marking-sent an outbox row before delivery is confirmed
- unbounded outbox table growth with no cleanup job
