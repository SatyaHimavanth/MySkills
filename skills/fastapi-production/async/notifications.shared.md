# Email / Notification Delivery — Shared

## Purpose
`security/passwords.shared.md` covers the security properties of a password-reset *token* (randomness, scoping, single-use). Nothing elsewhere covers actually delivering the email that carries it — provider integration, retry on failure, dead-lettering. A backend with a "forgot password" flow needs both halves; this is the missing one.

## Enqueue in the same transaction as the business write
Same reasoning as `async/outbox.shared.md`: create the notification row in the same DB transaction as the event that triggers it (e.g. password-reset token creation), not as a separate step that can fail independently and silently lose the notification.

```sql
CREATE TABLE notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  notification_type text NOT NULL,
  recipient text NOT NULL,
  template text NOT NULL,
  context jsonb NOT NULL,
  status text NOT NULL DEFAULT 'pending',
  attempts int NOT NULL DEFAULT 0,
  max_attempts int NOT NULL DEFAULT 5,
  next_attempt_at timestamptz NOT NULL DEFAULT now(),
  last_error text,
  created_at timestamptz NOT NULL DEFAULT now(),
  sent_at timestamptz
);
```

## Worker: retry with backoff, dead-letter on exhaustion
Verified end-to-end against real PostgreSQL with a provider stub that fails twice then succeeds, and a separate scenario forcing exhaustion: `FOR UPDATE SKIP LOCKED` for the same multi-worker safety as the outbox relay, exponential backoff via `make_interval()` (not string concatenation — `asyncpg` will reject an implicit int→text coercion there), and a hard `max_attempts` ceiling before dead-lettering instead of retrying forever.

```python
async def worker_tick(session):
    result = await session.execute(text(
        "SELECT id, recipient, template, attempts, max_attempts FROM notifications "
        "WHERE status = 'pending' AND next_attempt_at <= now() "
        "ORDER BY created_at LIMIT 10 FOR UPDATE SKIP LOCKED"
    ))
    for row in result.fetchall():
        try:
            await send_email(row.recipient, row.template, ...)
            await session.execute(text(
                "UPDATE notifications SET status = 'sent', sent_at = now() WHERE id = :id"
            ), {"id": row.id})
        except Exception as e:
            new_attempts = row.attempts + 1
            if new_attempts >= row.max_attempts:
                await session.execute(text(
                    "UPDATE notifications SET status = 'dead_letter', attempts = :a, last_error = :err WHERE id = :id"
                ), {"a": new_attempts, "err": str(e), "id": row.id})
            else:
                backoff_seconds = 2 ** new_attempts
                await session.execute(text(
                    "UPDATE notifications SET attempts = :a, last_error = :err, "
                    "next_attempt_at = now() + make_interval(secs => :backoff) WHERE id = :id"
                ), {"a": new_attempts, "err": str(e), "id": row.id, "backoff": backoff_seconds})
    await session.commit()
```
Verified: a notification still within its backoff window is correctly skipped by the next poll (not retried early), and dead-lettered notifications stop being picked up entirely rather than retrying forever.

## Provider choice
Any transactional-email provider (SES, Postmark, SendGrid, Resend) works behind this pattern — the retry/backoff/dead-letter logic is provider-agnostic by design, matching this skill's usual "swap the backend via config" principle. Don't call the provider synchronously inside the request handler that triggers the notification — that couples request latency to a third-party API's latency and turns a transient provider outage into a failed user-facing request instead of a queued retry.

## Templating
Keep templates out of application code (separate files/a template store), version them, and never interpolate untrusted user input directly into an HTML email template without escaping — the same injection class as `security/csrf.shared.md`'s concerns, applied to email rendering instead of a browser.

## Forbidden
- sending synchronously inside the request/response cycle
- no `max_attempts` ceiling (retrying a permanently-failing send forever)
- string-concatenating a backoff duration into SQL instead of `make_interval()`/parameterized interval construction
- silently dropping a notification on failure with no dead-letter visibility
- logging full email content (PII) at a verbosity level that ships to a shared log aggregator without redaction
