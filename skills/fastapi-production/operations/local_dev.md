# Operations — Local Development

## Purpose

Keep local operations lightweight while allowing failure modes to be exercised without requiring a full production platform.

## Local expectations

- Formal SLO enforcement is not required.
- Runbooks may use developer-friendly commands.
- Use local PostgreSQL/Redis only when the feature under test requires their real semantics.
- Test graceful degradation through deliberately stopped local dependencies where practical.

## Suggested local drills

```text
stop Redis
  → verify cache fallback
stop external mock
  → verify timeout/error mapping
exhaust test queue
  → verify bounded producer behavior
terminate worker
  → verify job retry/recovery semantics
```

Do not require a cloud load balancer, WAF, or multi-region stack for normal local development.
