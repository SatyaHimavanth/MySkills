# Webhook Signature Verification — Shared

## Purpose
`http/clients.shared.md` covers outbound HTTP calls thoroughly. This covers the reverse direction — receiving a webhook from a third party (payment provider, SaaS integration) and verifying it's genuine before acting on it. An unverified webhook endpoint lets anyone who finds the URL trigger arbitrary application logic by POSTing a forged payload.

## Signature pattern (Stripe-style, widely adopted)
Sign the timestamp and payload together, not the payload alone — otherwise a captured valid signature can be replayed against a different payload indefinitely. Verified directly, end-to-end against a real FastAPI endpoint:

```python
import hashlib
import hmac
import time
from fastapi import HTTPException

REPLAY_TOLERANCE_SECONDS = 300

def verify_webhook_signature(payload: bytes, signature_header: str, secret: str) -> None:
    try:
        parts = dict(p.split("=", 1) for p in signature_header.split(","))
        timestamp = parts["t"]
        provided_sig = parts["v1"]
        timestamp_int = int(timestamp)
    except (ValueError, KeyError):
        # Any malformed header must fail as a clean 400, not an unhandled exception.
        # Verified: a naive dict-comprehension parse crashes with an uncaught ValueError
        # on a header with no '=' at all, surfacing as an unhandled 500 — a stack trace
        # leaking to an untrusted caller, and a worse failure mode than the thing being
        # guarded against.
        raise HTTPException(400, "malformed signature header")

    if abs(time.time() - timestamp_int) > REPLAY_TOLERANCE_SECONDS:
        raise HTTPException(400, "timestamp outside tolerance — possible replay")

    signed_payload = f"{timestamp}.".encode() + payload
    expected_sig = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()

    # Constant-time comparison — a naive == leaks timing information about how many
    # leading bytes matched, letting an attacker binary-search the correct signature.
    if not hmac.compare_digest(expected_sig, provided_sig):
        raise HTTPException(400, "signature mismatch")
```

Verify against the **raw request body bytes**, read before any JSON parsing — re-serializing a parsed body and signing that can produce different bytes than what was actually signed (key ordering, whitespace), causing valid webhooks to fail verification.

## Signature verification is not idempotency
Verified directly: a genuinely valid, still-fresh signature can be replayed within the tolerance window and passes verification both times — signature checking proves authenticity, not uniqueness. A provider's *own* retry behavior (most webhook providers retry on anything but a 2xx) means the same event WILL arrive more than once under normal operation, not just under attack. Handle this with the same idempotency-key pattern as `async/idempotency.shared.md` — store processed event IDs and skip reprocessing, don't rely on the signature check alone.

## Forbidden
- verifying a re-serialized/re-parsed body instead of the raw bytes actually received
- signing the payload alone without the timestamp (enables indefinite replay of a captured signature)
- naive `==` comparison instead of `hmac.compare_digest` (timing side-channel)
- unbounded replay tolerance window
- treating "signature verified" as "safe to process without idempotency handling"
- letting a malformed/missing signature header raise an unhandled exception instead of a clean 400
