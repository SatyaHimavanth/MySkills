# Operations — Production

## Purpose

Apply reliability controls operationally in production.

## Required operational artifacts

- service SLOs/SLIs
- error-budget policy
- actionable alerts
- deployment/rollback procedure
- database backup/restore policy
- critical dependency runbooks
- ownership/escalation path

## Deployment readiness

Before production:

```text
build
 ↓
test
 ↓
validate migration
 ↓
canary/staged rollout where supported
 ↓
observe SLO/health signals
 ↓
expand rollout
```

## Incident response

Use the relevant runbook first. Avoid making multiple unrelated changes during an incident because it becomes impossible to tell which change restored service.

## Recovery

Recovery procedures must be tested periodically, not merely documented.
