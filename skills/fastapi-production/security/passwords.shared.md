# Passwords — Shared

## Purpose

Define secure password hashing, verification, reset, and rehashing behavior for application-owned credentials using `pwdlib` (Argon2id), unique salts, and optional application peppers.

## Rules

- Never store plaintext passwords.
- Use `pwdlib` (`PasswordHash.recommended()`) with **Argon2id** as the default password hashing algorithm (`passlib` is deprecated).
- **Salt**: Argon2id generates a cryptographically secure 128-bit unique salt automatically for every password hash.
- **Pepper**: If an application pepper is used, it must be stored in secure configuration (Pydantic Settings / Environment) separately from the database and combined with the password before hashing.
- Never weaken password rules or hashing cost parameters for developer convenience.

## Hashing with Salt & Pepper (`pwdlib`)

```python
import hmac
import hashlib
from pwdlib import PasswordHash
from pydantic_settings import BaseSettings
from pydantic import SecretStr

password_hash = PasswordHash.recommended()

def get_peppered_password(password: str, pepper: SecretStr) -> str:
    """Combines raw password with pepper using HMAC-SHA256 before Argon2 hashing."""
    return hmac.new(
        pepper.get_secret_value().encode("utf-8"),
        password.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def hash_password(password: str, pepper: SecretStr) -> str:
    peppered = get_peppered_password(password, pepper)
    # Argon2id generates a unique per-password salt automatically inside the hash string
    return password_hash.hash(peppered)

def verify_password(plain_password: str, hashed_password: str, pepper: SecretStr) -> bool:
    peppered = get_peppered_password(plain_password, pepper)
    return password_hash.verify(peppered, hashed_password)
```

## Migration and Rehashing

Password hashing parameters should be treated as a policy that can evolve. When a verified password uses an outdated parameter set, `pwdlib` checks if rehashing is needed (`password_hash.check_needs_rehash(hash)`). Rehash it using the current policy and update the stored hash in PostgreSQL after successful authentication.

## Credential-Reset Safety

## The same slowness that stops offline cracking is a CPU-DoS surface online
Argon2id's cost is deliberate and correct — it makes offline brute-forcing a stolen hash expensive. That same cost means every login request, legitimate or attacker-driven, consumes real CPU before it can be accepted or rejected. A flood of login requests is therefore also a CPU-exhaustion attack, not just a rate problem — see `operations/runbooks.shared.md`'s credential-stuffing runbook and `security/ratelimiting.shared.md`'s global circuit breaker. Never respond to that kind of incident by lowering the hash cost; fix the request volume reaching the hash, not the hash itself.

## Offload hashing/verification to a threadpool inside async routes
`password_hash.hash()` and `.verify()` are synchronous, CPU-bound calls (~100-200ms with `PasswordHash.recommended()`'s Argon2id parameters — measured directly). Calling either one directly inside an `async def` route or service method runs it on the event loop thread with nothing to yield control back to asyncio until it returns, so it delays every other concurrently in-flight request on that worker for its full duration — not just other auth requests, any request the same worker happens to be serving. Offload it:

```python
from starlette.concurrency import run_in_threadpool  # or: import anyio; await anyio.to_thread.run_sync(...)

hashed = await run_in_threadpool(password_hash.hash, peppered)
valid = await run_in_threadpool(password_hash.verify, peppered, stored_hash)
```

This buys event-loop *responsiveness* (other requests keep being served while a hash runs on a worker thread) — it does not buy hashing *throughput*. The hash itself is still bounded by available CPU: on a single-vCPU container, several concurrent hashes still compete for the same core and each individual hash still takes its full ~100-200ms; offloading only stops that cost from stalling unrelated work. Size worker/replica CPU allocation with that in mind for auth-heavy endpoints rather than assuming threadpool offload alone fixes throughput under load.

Password reset workflows should not disclose whether an account exists through response wording, timing, or email behavior. Use dummy verification timing for non-existent accounts. Reset tokens must be cryptographically random, short-lived, scoped to the reset operation, and invalidated after successful use.

## Forbidden

- storing plaintext or weak MD5/SHA1/SHA256 hashed passwords
- hardcoding password peppers in source code or storing them in the same database table as password hashes
- using unmaintained `passlib` or legacy `crypt` module (removed in Python 3.13)
- leaking account existence on password reset or login endpoints
- calling `password_hash.hash()`/`.verify()` directly inside an `async def` without offloading to a threadpool — blocks the event loop for every other concurrently in-flight request, not just auth requests
