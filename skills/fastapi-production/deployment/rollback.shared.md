# Rollback and Release Safety — Shared

## Purpose

Make failed deployments recoverable without creating database or data inconsistencies.

## Rollback priority

When user impact occurs:

```text
stabilize service
    ↓
stop harmful change
    ↓
rollback application when safe
    ↓
repair/migrate data separately
    ↓
verify recovery
```

Do not automatically roll back database schema changes as if they were application binaries.

## Application rollback

Prefer deployments where an older application version can run against the current schema when rolling back.

This is another reason expand-and-contract database migrations are required.

## Database rollback

Before destructive migrations, determine whether the change is reversible.

Often the safe response is a forward fix rather than an immediate schema downgrade.

## Release gates

Before production release:

- tests pass
- migration validation passes
- OpenAPI contract is reviewed
- health/readiness checks work
- critical dependency configuration is valid
- rollback procedure is known

## Canary / staged rollout

Where the platform supports it, reduce blast radius by exposing a new version to a smaller portion of traffic first.

Monitor:

- error rate
- latency
- dependency errors
- resource use
- business-critical SLIs

Increase traffic only when the release is healthy.

## Rollback trigger

Define objective triggers before deployment, such as:

```text
5xx above agreed threshold
SLO burn rate above agreed threshold
critical business operation failures
severe resource saturation
```

Do not make the release author decide after the fact whether the failure is "bad enough".

## Forbidden patterns

- rollback application while leaving it incompatible with schema
- irreversible data deletion without explicit recovery planning
- assuming `git revert` reverses database state
- deploying without a rollback/forward-fix decision
