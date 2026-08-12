# Idempotency — Shared

## Purpose

Make retried mutating requests and repeated message delivery safe without pretending networks or queues provide exactly-once execution. OWASP's current Secure by Design guidance recommends idempotent handlers and stable identifiers/deduplication for retries and duplicate delivery.

## Required policy

Every mutating endpoint must be classified as naturally idempotent or explicitly idempotent. Non-idempotent operations such as payments, job creation, voucher issuance, or external side effects should accept an `Idempotency-Key` when retry duplication is possible.

Example:

```http
POST /api/v1/payments
Idempotency-Key: 01JABC...
```

Define the key scope explicitly, for example `principal + endpoint + key` or `tenant + endpoint + key`.

## Replay semantics

Same key + same request fingerprint:

```text
replay the stored result; do not execute the side effect again
```

Same key + different request fingerprint:

```text
409 Conflict
```

Do not let each endpoint invent different semantics.

## Durable implementation

Use shared durable storage for multi-worker/multi-replica APIs. A PostgreSQL table is a strong default:

```text
idempotency_keys
principal_id
endpoint
key
request_hash
status
response_status
response_body
created_at
expires_at
```

Enforce a uniqueness constraint on the key scope. Use the database transaction/locking model to resolve concurrent duplicate requests; never use a process-local dictionary for correctness.

## Transaction boundary

Where business state and the idempotency record must change together:

```text
BEGIN
  reserve idempotency key
  perform business mutation
  persist replayable result
COMMIT
```

If the transaction fails, the key must not appear successfully completed.

## In-progress duplicate

Choose one project-wide policy:

- return a conflict while the original operation is running, or
- wait/replay when the original completes.

Document the policy and timeout behavior.

## External providers

For a non-idempotent external call, combine:

```text
incoming idempotency key
→ durable local dedupe
→ provider idempotency key when supported
```

Do not rely on the provider alone for protecting your own API state.

## Jobs/messages

Assume at-least-once delivery unless the chosen system explicitly provides another guarantee. Make worker effects idempotent using unique business keys, state transitions, processed-event IDs, or idempotency tables.

Do not promise exactly-once execution. Target exactly-once effects where business semantics permit it through durable deduplication + idempotent handlers.

## Retention

Define an explicit replay window. Purge expired idempotency records safely after that window.

## Tests

Test repeated requests, same-key/different-body conflict, concurrent duplicates, retry after timeout, response loss followed by retry, process restart, expiration, and partial business failure.

## Forbidden

- process-local idempotency state
- silent same-key/different-body acceptance
- assuming clients never retry
- `seen=true` without replay semantics
- treating idempotency as a replacement for transactions
