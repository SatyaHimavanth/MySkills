---
name: fastapi-production
description: Architecture guardrails for building production-grade FastAPI backends with PostgreSQL, Pydantic v2, SQLAlchemy 2.0, Argon2id, and multi-region deployment.
---

# FastAPI Production Skill

This skill is an implementation and architecture guardrail for coding assistants building production-grade FastAPI backends. It is designed to reduce architectural drift, environment-specific surprises, insecure shortcuts, and incompatible local/prod implementations.

## Global principles

1. PostgreSQL is the default database.
2. SQLite is allowed only when the user explicitly requests it; explain its limitations before choosing it.
3. Use `uv` for Python project and dependency management.
4. Use Pydantic Settings as the typed configuration boundary; do not scatter environment reads through application code.
5. Use Pydantic request/response models for API boundaries.
6. Local development should be production-shaped, not production-sized.
7. Discover the environment before choosing infrastructure.
8. Never silently substitute a compatibility-reduced fallback.
9. Inspect the existing project before introducing architecture or infrastructure.
10. Preserve stable API, DB, security, and operational contracts unless a deliberate change is reviewed and tested.
11. Prefer shared invariants plus local/prod implementation differences rather than duplicating business logic.
12. Treat security, concurrency, failure behavior, and observability as implementation requirements, not post-hoc hardening.

## Required agent workflow

```text
SCOPE THE PROJECT (if greenfield or ambiguous — see checklists/project-scoping.md)
  ↓
DISCOVER ENVIRONMENT
  ↓
INSPECT EXISTING PROJECT
  ↓
IDENTIFY CAPABILITY / REQUIREMENT
  ↓
READ relevant *.shared.md
  ↓
READ relevant *.local_dev.md / *.prod.md
  ↓
CHECK PRODUCTION INFLUENCE
  ↓
IMPLEMENT WITH EXISTING PROJECT CONVENTIONS
  ↓
RUN TARGETED TESTS
  ↓
RUN CONTRACT / SECURITY / PARITY CHECKS
  ↓
REVIEW BREAKING-CHANGE / MIGRATION IMPACT
  ↓
UPDATE DOCUMENTATION / ADR / COVERAGE WHEN NEEDED
```

## Environment discovery

Run only relevant safe checks before infrastructure-dependent work:

```bash
python --version
uv --version
git --version
docker --version
docker version
docker info
podman --version
podman info
psql --version
redis-server --version
```

An installed CLI is not proof that a runtime/service is usable. Never install, reconfigure, or grant system permissions automatically without user approval.

## Capability routing

| Capability | Read first |
|---|---|
| Project architecture | `architecture/shared.md`, `architecture/local_dev.md`, `architecture/prod.md` |
| Python/uv/dependencies | `python/uv.shared.md`, `python/uv.local_dev.md`, `python/uv.prod.md` |
| Configuration/settings | `configuration/shared.md` |
| Endpoints/routes | `api/endpoints.shared.md`, `api/endpoints.local_dev.md`, `api/endpoints.prod.md` |
| Request validation/resource limits | `validation/shared.md`, `validation/local_dev.md`, `validation/prod.md`, `api/resource_limits.shared.md` |
| Request/response schemas | `api/schemas.shared.md`, `api/response_contracts.shared.md`, `api/response_format.shared.md` |
| Pagination | `api/pagination.shared.md` |
| Versioning/inventory | `api/versioning.shared.md` |
| OpenAPI/docs | `api/openapi.shared.md`, `api/openapi.local_dev.md`, `api/openapi.prod.md` |
| Errors | `errors/shared.md`, `errors/local_dev.md`, `errors/prod.md` |
| PostgreSQL/SQLAlchemy | `database/shared.md`, `database/sessions.shared.md`, `database/acid.shared.md`, `database/transactions.shared.md`, `database/concurrency.shared.md`, `database/query_performance.shared.md`, `database/postgresql.shared.md`, `database/multi_region.shared.md` |
| Multi-tenancy | `database/multi_tenancy.shared.md` |
| Migrations | `database/migrations.shared.md`, `database/migrations.local_dev.md`, `database/migrations.prod.md` |
| Pooling/performance | `database/pooling.shared.md`, `database/performance.local_dev.md`, `database/performance.prod.md` |
| SQLite | `database/sqlite.local_dev.md` |
| Authentication | `security/authentication.shared.md`, `security/authentication.local_dev.md`, `security/authentication.prod.md` |
| Authorization | `security/authorization.shared.md`, `security/object_authorization.shared.md` |
| Passwords | `security/passwords.shared.md` |
| Rate limiting | `security/ratelimiting.shared.md`, `security/ratelimiting.local_dev.md`, `security/ratelimiting.prod.md` |
| SSRF | `security/ssrf.shared.md` |
| CSRF/cookies | `security/csrf.shared.md`, `security/csrf.local_dev.md`, `security/csrf.prod.md` |
| CORS / security headers / proxy trust | `security/cors.shared.md`, `security/cors.local_dev.md`, `security/cors.prod.md`, `security/security_headers.shared.md`, `security/security_headers.local_dev.md`, `security/security_headers.prod.md`, `security/http_security.shared.md`, `security/http_security.local_dev.md`, `security/http_security.prod.md`, `networking/routing.shared.md`, `networking/local_dev.md`, `networking/prod.md` |
| Secrets | `security/secrets.shared.md` |
| Audit logging | `security/audit_logging.shared.md` |
| PII protection at rest | `security/pii_protection.shared.md` |
| Middleware/request lifecycle | `middleware/shared.md`, `middleware/local_dev.md`, `middleware/prod.md`, `reliability/lifespan.shared.md`, `reliability/lifespan.local_dev.md`, `reliability/lifespan.prod.md` |
| Outbound HTTP | `http/clients.shared.md`, `http/clients.local_dev.md`, `http/clients.prod.md`, `http_client/shared.md` |
| Cache / Redis / Infrastructure | `cache/shared.md`, `cache/local_dev.md`, `cache/prod.md`, `infrastructure/containers.local_dev.md`, `infrastructure/containers.prod.md`, `infrastructure/fallbacks.local_dev.md` |
| Streaming/WebSockets | `streaming/shared.md` |
| Background jobs | `async/jobs.shared.md`, `async/local_dev.md`, `async/prod.md` |
| Transactional outbox / dual-write | `async/outbox.shared.md` |
| Idempotency | `async/idempotency.shared.md` |
| Storage/uploads/downloads | `storage/files.shared.md`, `storage/downloads.shared.md`, `storage/local_dev.md`, `storage/prod.md` |
| Time/date | `time/shared.md`, `time/local_dev.md`, `time/prod.md` |
| Testing | `testing/shared.md`, `testing/fixtures.shared.md`, `testing/database.shared.md`, `testing/api.shared.md`, `testing/security.shared.md`, `testing/contract.shared.md`, `testing/concurrency.shared.md`, `testing/e2e.shared.md`, `testing/local_dev.md`, `testing/prod.md` |
| Observability | `observability/shared.md`, `observability/local_dev.md`, `observability/prod.md` |
| Deployment/topology | `deployment/local_dev.md`, `deployment/prod.md`, `deployment/topology.shared.md`, `deployment/load_balancing.local_dev.md`, `deployment/load_balancing.prod.md` |
| CI/CD | `deployment/cicd.shared.md` |
| Reliability/degradation | `reliability/shared.md`, `reliability/degradation.shared.md`, `reliability/circuit_breakers.shared.md` |
| SLOs/alerting/DR/runbooks | `operations/slo.shared.md`, `operations/alerting.shared.md`, `operations/disaster_recovery.shared.md`, `operations/runbooks.shared.md`, `operations/local_dev.md`, `operations/prod.md` |
| Rollback | `deployment/rollback.shared.md` |
| Checklists | `checklists/project-scoping.md`, `checklists/new-endpoint.md`, `checklists/production-readiness.md`, `checklists/architecture-change.md`, `checklists/project-environment-discovery.md` |

## Environment rule

Do not create separate business logic for local and production merely because infrastructure differs. Prefer the same application contracts/interfaces with environment-specific infrastructure wiring.

## Compatibility fallback rule

Classify fallbacks as:

- `FULL`: semantics sufficiently match production for the feature under test
- `PARTIAL`: useful for development but cannot prove production behavior
- `MOCK`: only for isolated unit tests or non-semantic code paths

Never call a PARTIAL or MOCK fallback production-equivalent.

## PostgreSQL rule

Use PostgreSQL by default. If the user explicitly chooses SQLite for local development, read `database/sqlite.local_dev.md` and explain the limitations before implementing it.

## uv rule

Use:

- `[project].dependencies` for required runtime dependencies
- `[project.optional-dependencies]` for optional application extras
- `[dependency-groups]` for development tooling/groups

Use `uv add`, `uv remove`, `uv sync`, `uv run`, and locked CI workflows.

## Verification rule

A task is not complete merely because code runs locally. Verify the relevant API contract, database behavior, security boundary, tests, environment-specific behavior, and production influence.
