# Testing — Production / Release Validation

## Purpose

Define the minimum verification required before production rollout.

## Release gates

```text
lint/type checks
  ↓
unit
  ↓
API/contract
  ↓
security
  ↓
database/migrations
  ↓
integration
  ↓
E2E/smoke where applicable
  ↓
deploy
  ↓
post-deploy readiness/smoke
```

## Production parity

Release validation must use production-compatible infrastructure for behavior that depends on it:

```text
PostgreSQL → PostgreSQL
Redis semantics → Redis
object storage semantics → compatible object storage/provider
OIDC → test/sandbox IdP
```

## Post-deploy checks

Verify:

- readiness
- representative API route
- authentication
- DB access
- cache if required
- queue/job submission if required
- observability

## Rollback

The test/release process should define how to verify rollback compatibility, especially after schema migrations.

## Forbidden

- declaring production ready based only on unit tests
- using SQLite as the sole release database test
- skipping migration tests
- ignoring security-test failures
