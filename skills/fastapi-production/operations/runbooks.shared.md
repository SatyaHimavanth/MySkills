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

## Post-incident

Record:

- timeline
- customer impact
- root/contributing causes
- detection gaps
- mitigation success
- corrective actions

Do not turn the postmortem into a blame exercise.
