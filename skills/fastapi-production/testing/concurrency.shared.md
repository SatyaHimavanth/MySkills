# Concurrency Testing — Shared

## Purpose

Prove behavior when requests race, workers overlap, retries happen, or multiple consumers execute the same job.

## Required cases where relevant

- duplicate requests
- idempotency-key races
- optimistic version conflicts
- row-lock contention
- unique-constraint races
- rate-limit races
- duplicate job delivery
- cancellation races

## Test pattern

Use barriers/events rather than arbitrary sleeps.

Conceptual shape:

```text
worker A ─┐
          ├→ synchronized contention point
worker B ─┘
          ↓
assert one winner / defined conflict
```

## Database

Use real PostgreSQL for locking/isolation tests.

## Distributed services

Use real Redis/queue infrastructure when proving distributed semantics.

## Assertions

Assert the invariant, not the schedule.

Good:

```text
exactly one inventory reservation succeeds
```

Bad:

```text
worker A always completes before worker B
```

The second test encodes an accidental scheduler assumption.

## Flakiness

A flaky concurrency test is not evidence that the race is harmless. Stabilize synchronization or redesign the assertion around the invariant.
