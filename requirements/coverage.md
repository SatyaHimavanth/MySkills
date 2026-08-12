# Requirements Coverage Matrix

A requirement is complete only when its policy files exist, are routed from `SKILL.md` or a phase matrix, contain actionable implementation rules, and have local/prod treatment where the environment affects behavior.

| Requirement | Primary file(s) | Shared | Local | Prod | Discovery | Fallback | Status |
|---|---|---:|---:|---:|---:|---:|---|
| PostgreSQL default | database/shared.md, database/local_dev.md, database/prod.md | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETE |
| SQLite explicit-only + limitations | database/sqlite.local_dev.md | ✓ | ✓ | — | — | ✓ | COMPLETE |
| uv dependency management | python/uv.shared.md, python/uv.local_dev.md, python/uv.prod.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Environment discovery | checklists/project-environment-discovery.md | ✓ | ✓ | — | ✓ | ✓ | COMPLETE |
| Typed settings/.env | configuration/shared.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Endpoint management | api/endpoints.shared.md, api/endpoints.local_dev.md, api/endpoints.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Validation/resource limits | validation/shared.md, validation/local_dev.md, validation/prod.md, api/resource_limits.shared.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Request/response schemas | api/schemas.shared.md, api/response_contracts.shared.md, api/response_format.shared.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Pagination | api/pagination.shared.md | ✓ | — | — | — | — | COMPLETE |
| API versioning/inventory | api/versioning.shared.md | ✓ | — | — | — | — | COMPLETE |
| OpenAPI/documentation | api/openapi.shared.md, api/openapi.local_dev.md, api/openapi.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Error handling | errors/shared.md, errors/local_dev.md, errors/prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Authentication | security/authentication.shared.md, security/authentication.local_dev.md, security/authentication.prod.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Authorization/BOLA/property/function | security/authorization.shared.md, security/object_authorization.shared.md | ✓ | ✓ via tests | ✓ via policy | — | — | COMPLETE |
| Passwords | security/passwords.shared.md | ✓ | — | — | — | — | COMPLETE |
| Rate limiting | security/ratelimiting.shared.md, security/ratelimiting.local_dev.md, security/ratelimiting.prod.md | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETE |
| CORS | security/cors.shared.md, security/cors.local_dev.md, security/cors.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Security headers | security/security_headers.shared.md, security/security_headers.local_dev.md, security/security_headers.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| CSRF | security/csrf.shared.md, security/csrf.local_dev.md, security/csrf.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| SSRF | security/ssrf.shared.md | ✓ | — | — | ✓ | — | COMPLETE |
| Secrets | security/secrets.shared.md | ✓ | via config | ✓ | — | — | COMPLETE |
| Proxy/network trust | networking/routing.shared.md, networking/local_dev.md, networking/prod.md, security/http_security.*.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Middleware | middleware.shared.md, middleware.local_dev.md, middleware.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Lifespan/resources | reliability/lifespan.shared.md, reliability/lifespan.local_dev.md, reliability/lifespan.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| SQLAlchemy sessions | database/shared.md, database/sessions.shared.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| ACID/transactions/isolation | database/acid.shared.md, database/transactions.shared.md | ✓ | — | ✓ | — | — | COMPLETE |
| Concurrency/locking | database/concurrency.shared.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Connection pooling | database/pooling.shared.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Migrations | database/migrations.shared.md, database/migrations.local_dev.md, database/migrations.prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Query performance | database/query_performance.shared.md, database/performance.local_dev.md, database/performance.prod.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| PostgreSQL features | database/postgresql.shared.md | ✓ | — | — | — | — | COMPLETE |
| Time/date | time/shared.md, time/local_dev.md, time/prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Outbound HTTP | http/clients.shared.md, http/clients.local_dev.md, http/clients.prod.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Idempotency | async/idempotency.shared.md | ✓ | via tests | via policy | — | — | COMPLETE |
| Background jobs | async/jobs.shared.md, async/local_dev.md, async/prod.md | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETE |
| Streaming/WebSockets | streaming/shared.md | ✓ | via testing | via deployment | — | PARTIAL local infrastructure | COMPLETE |
| Caching | cache/shared.md, cache/local_dev.md, cache/prod.md | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETE |
| Redis/infrastructure detection | infrastructure/containers.local_dev.md, infrastructure/fallbacks.local_dev.md | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETE |
| Storage/uploads/downloads | storage/files.shared.md, storage/downloads.shared.md, storage/local_dev.md, storage/prod.md | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETE |
| Observability | observability/shared.md, observability/local_dev.md, observability/prod.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Testing architecture | testing/*.md | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETE |
| Deployment/topology/load balancing | deployment/topology.shared.md, deployment/load_balancing.local_dev.md, deployment/load_balancing.prod.md, deployment/prod.md | ✓ | ✓ | ✓ | ✓ | — | COMPLETE |
| Reliability/degradation/circuit breakers | reliability/shared.md, reliability/degradation.shared.md, reliability/circuit_breakers.shared.md | ✓ | ✓ | ✓ | — | ✓ | COMPLETE |
| SLO/alerting/DR/runbooks | operations/*.md | ✓ | ✓ | ✓ | — | — | COMPLETE |
| Rollback | deployment/rollback.shared.md | ✓ | — | ✓ | — | — | COMPLETE |

## Release gate

A release package is valid only when:

- all rows are COMPLETE
- all `SKILL.md` references resolve
- all shared/local/prod policy documents have the required structure
- no internal/non-portable citation markup remains
- all phase verifiers pass
- `requirements/content_quality_audit.py` passes
- the final ZIP passes `unzip -t`
