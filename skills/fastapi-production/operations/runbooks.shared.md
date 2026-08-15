# Operational Runbooks — Shared

## Purpose

Give coding assistants a standard shape for operational procedures so incidents do not depend on tribal knowledge.

## Runbook structure

Every production-critical runbook should contain:

1. Scope
2. Symptoms
3. Impact
4. Detection/alerts
5. Preconditions
6. Safe first actions
7. Investigation commands/queries
8. Mitigation
9. Recovery
10. Verification
11. Escalation
12. Follow-up

## Initial incident behavior

Prefer mitigation over speculative root-cause changes.

Examples:

```text
high error rate
  → inspect recent deploy
  → inspect dependency health
  → verify DB/cache saturation
  → consider rollback/canary stop
```

## Database outage runbook

Check:

- PostgreSQL availability
- connection count
- pool exhaustion
- recent migrations
- network path
- application error rate

Do not repeatedly restart all API instances without evidence; this can amplify connection pressure.

## Redis outage runbook

Determine the feature:

```text
cache → likely degrade/fail open
rate limit → explicit policy
lock → safety-critical policy
queue → job durability policy
```

Do not treat every Redis outage as equivalent.

## Queue backlog runbook

Check:

- queue depth
- oldest job age
- worker health
- worker concurrency
- dependency latency
- retry storm

Mitigate producer overload before blindly adding workers.

## High memory runbook

Check:

- recent deploy
- request/file sizes
- worker count
- large in-memory responses
- cache growth
- queue/job payloads
- memory fragmentation/container limits

## Credential stuffing / login-flood runbook

Symptoms: high request volume on the login endpoint from many distinct IPs, CPU near 100%, legitimate users unable to log in.

Check:
- is this distributed across many IPs (evades per-IP limits by design) or concentrated (per-IP/per-username limits from `security/ratelimiting.shared.md` should already be absorbing it — if not, they're misconfigured or bypassed)
- CPU profile — a login-endpoint CPU spike is almost always the password hash itself (Argon2id is deliberately slow, see `security/passwords.shared.md`'s Forbidden note), not application logic; confirm the rate limiter check actually runs before the hash call, not after
- whether any WAF/CDN sits in front of the app at all, and whether it has an active rate-based rule or "under attack" mode available
- whether any attempts are succeeding (leaked-credential correlation) — turns this into an account-takeover incident, not just a DoS one

Mitigate:
- edge/WAF-level blocking or JS challenge first — this is materially cheaper than absorbing the flood in the app, since the app has already paid connection/TLS cost by the time it sees the request
- a global aggregate circuit breaker on the login endpoint, independent of the per-IP/per-username buckets — those are structurally blind to fan-out across many distinct IPs summing past capacity while each stays under its own threshold
- CAPTCHA/proof-of-work challenge after N failures, instead of a hard block, to filter bots without locking out legitimate users
- do not lower Argon2id's cost parameters to reduce CPU load — that weakens the credential store against offline cracking to solve an online-volume problem; fix the volume problem instead

Do not confuse this with a real capacity problem and respond by just scaling out — horizontal scaling absorbs legitimate load, it does not stop an attacker from sending more, and it's slow/expensive to provision against a CPU-bound hash workload specifically.

Post-incident: correlate targeted usernames against known credential-leak lists; force password resets on any account with a successful login during the window.

## Post-incident

Record:

- timeline
- customer impact
- root/contributing causes
- detection gaps
- mitigation success
- corrective actions

Do not turn the postmortem into a blame exercise.
