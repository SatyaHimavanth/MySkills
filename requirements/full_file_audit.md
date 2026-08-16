# Full File-by-File Audit

This audit was generated after reading every file in the release tree. It records basic structural evidence for each file and the release-wide checks applied to the complete tree.

- The table below is a historical audit snapshot and is not the authoritative current file count. Current counts should be derived from the filesystem and release verification scripts so the audit does not silently become stale after additions/renames.
- Empty files in the audited snapshot: 0

## File manifest

Note: `.dev/environment.local.md` is intentionally **not** listed below. It is a runtime artifact the coding agent creates inside the *consumer's* project (see `checklists/project-environment-discovery.md`), not a file shipped in this repository. An earlier snapshot of this audit incorrectly listed it as a tracked release file; that row has been removed.

| File | Bytes | Lines | First heading | Structural status |
|---|---:|---:|---|---|
| `.gitignore` | 45 | 0 |  | PASS |
| `SKILL.md` | 8718 | 164 | FastAPI Production Skill | PASS |
| `api/endpoints.local_dev.md` | 768 | 26 | Endpoint Management — Local Development | PASS |
| `api/endpoints.prod.md` | 740 | 18 | Endpoint Management — Production | PASS |
| `api/endpoints.shared.md` | 975 | 27 | API Endpoints | PASS |
| `api/openapi.local_dev.md` | 955 | 15 | OpenAPI — Local Development | PASS |
| `api/openapi.prod.md` | 946 | 15 | OpenAPI — Production | PASS |
| `api/openapi.shared.md` | 1081 | 31 | OpenAPI and API Documentation | PASS |
| `api/pagination.shared.md` | 520 | 20 | Pagination | PASS |
| `api/resource_limits.shared.md` | 1997 | 81 | API Resource Limits — Shared | PASS |
| `api/response_contracts.shared.md` | 1536 | 46 | API Response Contracts | PASS |
| `api/response_format.shared.md` | 693 | 29 | Response Format | PASS |
| `api/schemas.shared.md` | 932 | 31 | API Schemas | PASS |
| `api/versioning.shared.md` | 1861 | 85 | API Versioning and Inventory — Shared | PASS |
| `architecture/local_dev.md` | 747 | 21 | Architecture: Local Development | PASS |
| `architecture/prod.md` | 708 | 20 | Architecture: Production | PASS |
| `architecture/scale_tiers.shared.md` | 6738 | 61 | Scale Tiers — Shared | PASS |
| `architecture/shared.md` | 708 | 20 | Architecture | PASS |
| `async/idempotency.shared.md` | 3151 | 111 | Idempotency — Shared | PASS |
| `async/jobs.shared.md` | 3073 | 114 | Background Jobs — Shared | PASS |
| `async/local_dev.md` | 1309 | 34 | Distributed Runtime — Local Development | PASS |
| `async/prod.md` | 1029 | 22 | Distributed Runtime — Production | PASS |
| `cache/local_dev.md` | 720 | 32 | Caching — Local Development | PASS |
| `cache/prod.md` | 901 | 33 | Caching — Production | PASS |
| `cache/shared.md` | 2228 | 101 | Caching — Shared | PASS |
| `checklists/architecture-change.md` | 525 | 15 | Architecture Change Checklist | PASS |
| `checklists/new-endpoint.md` | 441 | 16 | New Endpoint Checklist | PASS |
| `checklists/production-readiness.md` | 446 | 13 | Production Readiness Checklist | PASS |
| `checklists/project-environment-discovery.md` | 769 | 21 | Project Environment Discovery Checklist | PASS |
| `configuration/shared.md` | 825 | 26 | Configuration | PASS |
| `database/acid.shared.md` | 1601 | 35 | ACID and Transaction Correctness | PASS |
| `database/concurrency.shared.md` | 1759 | 49 | Database Concurrency | PASS |
| `database/local_dev.md` | 1234 | 34 | Database: Local Development | PASS |
| `database/migrations.local_dev.md` | 642 | 20 | Database Migrations — Local Development | PASS |
| `database/migrations.prod.md` | 610 | 13 | Database Migrations — Production | PASS |
| `database/migrations.shared.md` | 1720 | 54 | Database Migrations — Shared | PASS |
| `database/query_performance.local_dev.md` | 1384 | 39 | Database Performance — Local Development | PASS |
| `database/query_performance.prod.md` | 1928 | 49 | Database Performance — Production | PASS |
| `database/pooling.shared.md` | 2243 | 92 | Database Connection Pooling — Shared | PASS |
| `database/postgresql.shared.md` | 1941 | 54 | PostgreSQL-Specific Design | PASS |
| `database/prod.md` | 1206 | 36 | Database: Production | PASS |
| `database/query_performance.shared.md` | 1343 | 31 | Database Query Performance | PASS |
| `database/sessions.shared.md` | 2152 | 53 | SQLAlchemy Session Lifecycle — Shared | PASS |
| `database/shared.md` | 1755 | 65 | Database — Shared | PASS |
| `database/sqlite.local_dev.md` | 687 | 21 | Database: SQLite Local Development | PASS |
| `database/transactions.shared.md` | 1352 | 30 | Transactions | PASS |
| `deployment/load_balancing.local_dev.md` | 606 | 30 | Load Balancing — Local Development | PASS |
| `deployment/load_balancing.prod.md` | 871 | 41 | Load Balancing — Production | PASS |
| `deployment/local_dev.md` | 977 | 33 | Deployment: Local Development | PASS |
| `deployment/prod.md` | 1199 | 38 | Deployment: Production | PASS |
| `deployment/rollback.shared.md` | 1919 | 81 | Rollback and Release Safety — Shared | PASS |
| `deployment/topology.shared.md` | 1626 | 65 | Deployment Topology — Shared | PASS |
| `errors/local_dev.md` | 708 | 26 | Error Handling — Local Development | PASS |
| `errors/prod.md` | 745 | 32 | Error Handling — Production | PASS |
| `errors/shared.md` | 821 | 24 | Error Handling | PASS |
| `http/clients.local_dev.md` | 895 | 28 | Outbound HTTP — Local Development | PASS |
| `http/clients.prod.md` | 781 | 24 | Outbound HTTP — Production | PASS |
| `http/clients.shared.md` | 3281 | 89 | Outbound HTTP Clients — Shared | PASS |
| `infrastructure/containers.local_dev.md` | 892 | 31 | Containers: Local Development | PASS |
| `infrastructure/fallbacks.local_dev.md` | 1023 | 34 | Local Fallbacks | PASS |
| `memory.md` | 18664 | 327 | FastAPI Production Skill Memory | PASS |
| `middleware/local_dev.md` | 755 | 23 | Middleware — Local Development | PASS |
| `middleware/prod.md` | 805 | 25 | Middleware — Production | PASS |
| `middleware/shared.md` | 1212 | 54 | Middleware — Shared | PASS |
| `networking/local_dev.md` | 633 | 26 | Networking — Local Development | PASS |
| `networking/prod.md` | 669 | 19 | Networking — Production | PASS |
| `networking/routing.shared.md` | 885 | 30 | Networking and Proxy Routing — Shared | PASS |
| `observability/local_dev.md` | 860 | 31 | Observability — Local Development | PASS |
| `observability/prod.md` | 1264 | 60 | Observability — Production | PASS |
| `observability/shared.md` | 2277 | 75 | Observability — Shared | PASS |
| `operations/alerting.shared.md` | 1717 | 93 | Alerting — Shared | PASS |
| `operations/disaster_recovery.shared.md` | 2505 | 129 | Disaster Recovery — Shared | PASS |
| `operations/local_dev.md` | 822 | 31 | Operations — Local Development | PASS |
| `operations/prod.md` | 781 | 42 | Operations — Production | PASS |
| `operations/runbooks.shared.md` | 1768 | 101 | Operational Runbooks — Shared | PASS |
| `operations/slo.shared.md` | 2635 | 107 | SLOs, SLIs, and Error Budgets — Shared | PASS |
| `python/uv.local_dev.md` | 384 | 16 | uv — Local Development | PASS |
| `python/uv.prod.md` | 847 | 27 | uv — Production | PASS |
| `python/uv.shared.md` | 1216 | 37 | uv Package and Project Management | PASS |
| `reliability/circuit_breakers.shared.md` | 2035 | 102 | Circuit Breakers — Shared | PASS |
| `reliability/degradation.shared.md` | 4423 | 200 | Graceful Degradation and Failure Isolation — Shared | PASS |
| `reliability/lifespan.local_dev.md` | 1048 | 26 | Lifespan — Local Development | PASS |
| `reliability/lifespan.prod.md` | 1136 | 26 | Lifespan — Production | PASS |
| `reliability/lifespan.shared.md` | 2122 | 79 | Application Lifespan and Resource Ownership — Shared | PASS |
| `reliability/shared.md` | 1689 | 69 | Reliability — Shared | PASS |
| `requirements/content_consistency_audit.py` | 2393 | 59 | Explicit contradictions we never want in a completed skill. | PASS |
| `requirements/content_quality_audit.md` | 249 | 10 | Content Quality Audit | PASS |
| `requirements/content_quality_audit.py` | 1420 | 35 | Validate SKILL.md code-like relative markdown references, ignoring glob patterns. | PASS |
| `requirements/coverage.md` | 6502 | 64 | Requirements Coverage Matrix | PASS |
| `requirements/factcheck_audit.md` | 3375 | 50 | Final Fact-Check Audit | PASS |
| `requirements/phase1_coverage.md` | 838 | 12 | Phase 1 Coverage | PASS |
| `requirements/phase2_coverage.md` | 1094 | 17 | Phase 2 Coverage | PASS |
| `requirements/phase3_coverage.md` | 677 | 10 | Phase 3 Coverage | PASS |
| `requirements/phase4_coverage.md` | 1612 | 15 | Phase 4 Coverage Matrix | PASS |
| `requirements/phase5_coverage.md` | 1614 | 22 | Phase 5 Coverage | PASS |
| `requirements/phase6_coverage.md` | 1213 | 21 | Phase 6 Coverage | PASS |
| `requirements/phase7_coverage.md` | 876 | 14 | Phase 7 Coverage | PASS |
| `requirements/verify_coverage.py` | 1423 | 42 | Minimum substantive-file guard. Environment delta files may remain concise, | PASS |
| `requirements/verify_phase1.py` | 1123 | 38 |  | PASS |
| `requirements/verify_phase2.py` | 978 | 35 |  | PASS |
| `requirements/verify_phase3.py` | 1330 | 36 |  | PASS |
| `requirements/verify_phase4.py` | 1512 | 36 |  | PASS |
| `requirements/verify_phase5.py` | 1363 | 40 |  | PASS |
| `requirements/verify_phase6.py` | 2028 | 47 |  | PASS |
| `requirements/verify_phase7.py` | 1405 | 35 |  | PASS |
| `review_audit.md` | 1531 | 44 | Final Content and Consistency Audit | PASS |
| `security/api_security.shared.md` | 2648 | 137 | OWASP API Security Coverage — Shared | PASS |
| `security/authentication.local_dev.md` | 1428 | 51 | Authentication — Local Development | PASS |
| `security/authentication.prod.md` | 1369 | 40 | Authentication — Production | PASS |
| `security/authentication.shared.md` | 952 | 34 | Authentication | PASS |
| `security/authorization.shared.md` | 1624 | 82 | Authorization — Shared | PASS |
| `security/cors.local_dev.md` | 383 | 15 | CORS — Local Development | PASS |
| `security/cors.prod.md` | 619 | 19 | CORS — Production | PASS |
| `security/cors.shared.md` | 936 | 33 | CORS — Shared | PASS |
| `security/csrf.local_dev.md` | 1148 | 28 | CSRF — Local Development | PASS |
| `security/csrf.prod.md` | 1020 | 31 | CSRF — Production | PASS |
| `security/csrf.shared.md` | 4185 | 160 | CSRF Protection — Shared | PASS |
| `security/http_security.local_dev.md` | 794 | 24 | HTTP Security — Local Development | PASS |
| `security/http_security.prod.md` | 821 | 38 | HTTP Security — Production | PASS |
| `security/http_security.shared.md` | 1995 | 72 | HTTP Security Configuration — Shared | PASS |
| `security/object_authorization.shared.md` | 4262 | 192 | Object, Property, and Function Authorization — Shared | PASS |
| `security/passwords.shared.md` | 1048 | 40 | Passwords | PASS |
| `security/ratelimiting.local_dev.md` | 1086 | 31 | Rate Limiting — Local Development | PASS |
| `security/ratelimiting.prod.md` | 1131 | 43 | Rate Limiting — Production | PASS |
| `security/ratelimiting.shared.md` | 1101 | 54 | Rate Limiting | PASS |
| `security/secrets.shared.md` | 2442 | 120 | Secrets Management — Shared | PASS |
| `security/security_headers.local_dev.md` | 632 | 18 | Security Headers — Local Development | PASS |
| `security/security_headers.prod.md` | 690 | 19 | Security Headers — Production | PASS |
| `security/security_headers.shared.md` | 1052 | 32 | Security Headers — Shared | PASS |
| `security/ssrf.shared.md` | 5774 | 236 | SSRF Protection — Shared | PASS |
| `storage/downloads.shared.md` | 1125 | 78 | File Downloads — Shared | PASS |
| `storage/files.shared.md` | 8835 | 424 | File Handling and Upload Security — Shared | PASS |
| `storage/local_dev.md` | 1751 | 85 | File Storage — Local Development | PASS |
| `storage/prod.md` | 2506 | 125 | File Storage — Production | PASS |
| `streaming/shared.md` | 3065 | 90 | Streaming and WebSockets — Shared | PASS |
| `testing/api.shared.md` | 1740 | 90 | API Testing — Shared | PASS |
| `testing/concurrency.shared.md` | 1171 | 61 | Concurrency Testing — Shared | PASS |
| `testing/contract.shared.md` | 1146 | 46 | Contract Testing — Shared | PASS |
| `testing/database.shared.md` | 2700 | 108 | Database Testing — Shared | PASS |
| `testing/e2e.shared.md` | 892 | 33 | End-to-End Testing — Shared | PASS |
| `testing/fixtures.shared.md` | 1142 | 106 | Test Fixtures — Shared | PASS |
| `testing/local_dev.md` | 903 | 48 | Testing — Local Development | PASS |
| `testing/prod.md` | 1098 | 62 | Testing — Production / Release Validation | PASS |
| `testing/pyproject.toml.example` | 475 | 0 |  | PASS |
| `testing/security.shared.md` | 1736 | 97 | Security Testing — Shared | PASS |
| `testing/shared.md` | 6786 | 297 | Testing — Shared | PASS |
| `time/local_dev.md` | 600 | 20 | Time — Local Development | PASS |
| `time/prod.md` | 630 | 20 | Time — Production | PASS |
| `time/shared.md` | 685 | 19 | Time and Date Handling | PASS |
| `validation/local_dev.md` | 752 | 17 | Validation — Local Development | PASS |
| `validation/prod.md` | 785 | 18 | Validation — Production | PASS |
| `validation/shared.md` | 937 | 30 | Input Validation and Resource Limits | PASS |

## Fact-check basis

- FastAPI settings/dependency/yield/security/file-upload/testing/deployment documentation was checked against the current official FastAPI documentation.
- SQLAlchemy session, asyncio concurrency, relationship loading, pooling, versioning, and transaction guidance was checked against current SQLAlchemy 2.x documentation.
- Alembic migration guidance was checked against current Alembic documentation.
- uv dependency groups, optional extras, lock/sync behavior, and project workflow were checked against current uv documentation.
- HTTPX timeout/resource-limit/client guidance was checked against current HTTPX documentation.
- Python time-zone/UTC guidance was checked against current Python documentation.
- OpenTelemetry status/propagation guidance was checked against current OpenTelemetry Python documentation.
- PostgreSQL isolation/locking/explain/backup guidance was checked against current PostgreSQL documentation.
- API security guidance was checked against the current OWASP API Security Top 10 and relevant OWASP cheat sheets.
- Object-storage/presigned-URL guidance was checked against current AWS S3 documentation where provider-specific facts are discussed.

## Release gates

Run these from the skill root before packaging:

```bash
python requirements/verify_coverage.py
python requirements/verify_phase1.py
python requirements/verify_phase2.py
python requirements/verify_phase3.py
python requirements/verify_phase4.py
python requirements/verify_phase5.py
python requirements/verify_phase6.py
python requirements/verify_phase7.py
python requirements/content_quality_audit.py
python requirements/content_consistency_audit.py
```

All release gates passed for this audited tree.
