# FastAPI Production Skill Memory

This file records durable architecture decisions for the skill. It is not a substitute for the detailed reference files.

## Core decisions

- PostgreSQL is the default database.
- SQLite requires explicit user choice plus limitation disclosure.
- uv is the package/dependency manager.
- Pydantic Settings is the configuration boundary.
- Pydantic models define API request/response contracts.
- Local development is production-shaped, not production-sized.
- Environment discovery precedes infrastructure selection.
- Docker/Podman must never be assumed available or permitted.
- Python/local fallbacks are classified FULL/PARTIAL/MOCK.
- Shared rules are separated from local/prod rules.
- API, DB, security, and deployment contracts should not drift silently.
- Default production target is Tier 1 — small-team production (single region, ~100–1,000 users, a handful of replicas), not Tier 2 regional/global. See `architecture/scale_tiers.shared.md`. Multi-region/CDN topology requires a concrete escalation trigger.
- Cloud-provider provisioning (managed services, IAM, networking, DNS/CDN setup) is explicitly out of scope; that work belongs to the project's cloud-provider skill, invoked with the tier's requirements as input.
- `http/` is the single home for outbound HTTP client policy. The earlier duplicate `http_client/` folder was merged into `http/` and removed — do not recreate it.
- Tier 1 default tenancy is single-tenant (one internal org per deployment). Multi-tenancy (`database/multi_tenancy.shared.md`) is opt-in, applied only when a project genuinely serves multiple orgs from one deployment — not added speculatively at Tier 1.
- Verified end-to-end (real FastAPI app + real Orval-generated TS client, live HTTP calls, not mocks): a `@app.exception_handler(DomainError)` returning 409/401/429 is correct at runtime but invisible to `/openapi.json` unless each route declares those codes via `responses=`. Since `frontend-api-client` generates its error types from that schema, an undeclared status code silently produces an incomplete generated error type with zero warning from codegen. Fixed in `api/response_contracts.shared.md` (backend) and `frontend-api-client/codegen/shared.md` + `error-handling/shared.md` (frontend).
- Verified: Argon2id hashing (~100-200ms via `PasswordHash.recommended()`) must be offloaded to a threadpool (`run_in_threadpool`/`anyio.to_thread.run_sync`) inside async routes/services, or it blocks the event loop for the full hash duration. Documented in `security/passwords.shared.md`, including the caveat that offloading buys responsiveness, not hashing throughput — throughput is still bounded by available CPU cores.
- Verified: a stateful in-process singleton (e.g. the local rate limiter) must be exposed via a `Depends`-injected provider function, not imported as a bare module-level instance, or `testing/security.shared.md`'s required "independent principals"/"reset/expiry" rate-limit tests have no way to reset state between tests. Also verified a specific gotcha: a test override that *constructs* a fresh instance per call (instead of closing over one shared instance) silently defeats the limiter — the count never accumulates and the limit never trips. Documented in `security/ratelimiting.shared.md`, `security/ratelimiting.local_dev.md`, and cross-linked from `testing/security.shared.md`.
- Verified: PyJWT raises `InsecureKeyLengthWarning` for HS256 secrets under 32 bytes. The skill's own local-dev example secret (`development-only-secret`, 23 bytes) tripped this. Fixed the example in `security/authentication.local_dev.md` to be 32+ bytes and added a Forbidden entry.

## API

- Version APIs (`/api/v1/...`).
- Keep route handlers thin.
- Use response models and examples.
- Standardize errors, status codes, and pagination.
- Treat endpoint schemas and status codes as contracts.

## Database

- SQLAlchemy for DB access.
- Alembic for migrations.
- Explicit sessions and transaction boundaries.
- PostgreSQL integration tests for PostgreSQL-sensitive behavior.
- Pool sizing accounts for workers/replicas and DB connection budgets.
- Isolation/locking/concurrency decisions are explicit.

## Security

- Separate authentication and authorization.
- Use FastAPI `Security()` for scope-aware authorization where appropriate.
- Passwords are slow-hashed; never stored plaintext.
- CORS, cookies, CSRF, rate limits, and headers are explicit policies.

## Reliability

- FastAPI lifespan for app-wide resource startup/shutdown.
- Health/readiness/liveness are distinct concepts.
- Timeouts and bounded retries are explicit.
- BackgroundTasks is not a durable queue.

## Infrastructure

- Shared infrastructure state must not depend on one process.
- Redis is introduced only for a concrete use case.
- Cache, queue, storage, and locks have distinct semantics.
- Object storage is behind an interface.

## Async/jobs

- Streaming is a response-delivery mechanism, not durable processing.
- Long-running work uses durable jobs/queues.
- Job state, retry, idempotency, cancellation, and DB/queue consistency are explicit.

## Time/concurrency

- Use timezone-aware datetimes and UTC for persisted instants.
- Use IANA timezones for business-local time.
- Assume multiple workers/replicas when designing correctness.
- Prefer DB atomicity, locking, or optimistic concurrency over process-local synchronization.

## Architecture simplicity / promotion decisions

- Start from the smallest architecture that satisfies settled requirements.
- Production-shaped means preserving contracts, invariants, authorization, transaction semantics, resource ownership, failure behavior, and operational boundaries—not mirroring production infrastructure locally.
- Prefer a modular monolith for greenfield work unless independent deployment, scaling, ownership, or failure isolation is an explicit requirement.
- Add Redis, queues, object storage, service decomposition, multi-region infrastructure, or distributed coordination only when a concrete requirement needs their semantics.
- Preserve realistic replacement seams at infrastructure boundaries; do not introduce abstraction layers without a plausible future replacement point.
- Use `FULL` / `PARTIAL` / `MOCK` to state what local substitutes can and cannot prove.
- Every non-trivial architecture choice should record a short baseline, rationale, future production seam, escalation trigger, and known local PARTIAL behavior.
- Promotion should primarily change configuration, infrastructure wiring, scaling, and operations—not domain/business logic or public API contracts.

## Production topology

```text
Client
  ↓
Load balancer / reverse proxy
  ↓
FastAPI instances
  ↓
PostgreSQL + shared Redis/cache + queue + object storage
```

Local infrastructure may be smaller, but application semantics should remain compatible.

## Audit state

- The skill has passed the structural routing audit as of 2026-08-11.
- Greenfield/materially ambiguous work uses an explicit scoping gate and a complexity-budget gate before implementation; small, already-clear changes bypass both to avoid ceremony.
- 60 unique Markdown references from `SKILL.md` resolve to existing files.
- No non-exempt policy document is below the minimum substantive-content threshold enforced by `requirements/verify_coverage.py`.
- `review_audit.md` records the audit findings and remaining scope.
- Do not mark future requirements complete merely because a file exists; preserve the audit gate.

## Configuration quality decisions

- Use `pydantic-settings` as the single typed configuration boundary.
- Use nested Pydantic models for related configuration.
- Cache the settings dependency with `@lru_cache` rather than constructing Settings per request.
- Use the same Settings model in local/test/staging/production; change input sources and values, not the schema.
- Use `.env` for local development and external environment/secret injection for production.
- Use `SecretStr` for sensitive settings where practical and never dump Settings to logs.
- Required infrastructure settings must fail startup instead of silently falling back.
- Use `env_nested_delimiter="__"` for nested environment variables.
- Keep `.env.example` synchronized with the Settings model.

## API response contract decisions

- Every JSON endpoint needs an intentional Pydantic response model.
- Do not expose SQLAlchemy ORM objects directly as public contracts.
- Keep request and response schemas separate when their contracts differ.
- Status codes are part of the API contract.
- Use stable machine-readable error codes.
- Keep pagination shape consistent; choose offset or cursor based on scale and consistency requirements.
- Do not force streaming/binary protocols into JSON envelopes.
- Document meaningful non-success responses and OpenAPI examples.
- Treat breaking response changes as explicit versioning/migration decisions.

## Authentication quality decisions

- Identify the identity provider before implementing authentication.
- For application-owned password auth, prefer the current FastAPI PyJWT + pwdlib/Argon2 pattern.
- Use OAuth2PasswordBearer for bearer-token extraction and `Security()`/`SecurityScopes` for documented OAuth2 scopes.
- Validate JWT signature, algorithm, expiration, and issuer/audience where applicable.
- Keep access tokens short-lived and design refresh/revocation explicitly.
- Separate authentication, scopes/roles, and resource/tenant authorization.
- Use dummy-hash verification for nonexistent users to reduce login timing differences.
- Never log passwords, bearer tokens, refresh tokens, or signing secrets.

## Rate limiting quality decisions

- Rate limiting is resource protection, not merely authentication.
- Use gateway/WAF controls for coarse traffic protection and application-level limits for user/tenant/resource policies when needed.
- Never trust arbitrary forwarded client IP headers; establish a proxy trust boundary.
- Use shared Redis or equivalent state for quotas that must hold across workers/replicas.
- Make counter + expiry updates atomic; do not implement a naïve GET/INCR/EXPIRE sequence.
- Select fixed-window, sliding-window, or token-bucket algorithms based on actual requirements.
- Return `429` and a consistent error contract for rejected requests.
- Define fail-open/fail-closed behavior per policy when the limiter backend is unavailable.
- Local memory limiting is PARTIAL compatibility and does not prove distributed behavior.

## Cache quality decisions

- Distinguish application caching from HTTP response caching.
- Use cache-aside unless another pattern is deliberately justified.
- Cache keys must include every dimension that affects the result, including tenant/user/representation where relevant.
- Every cache entry needs a TTL or explicit invalidation strategy.
- Invalidate after the source-of-truth transaction commits.
- Treat cache failure differently from rate-limit/lock failure; do not use one global Redis failure policy.
- Prevent cache stampedes for hot expensive keys when necessary.
- Never cache ORM objects directly.
- Use shared Redis for multi-replica shared cache state.
- Local memory cache is PARTIAL compatibility only.

## Error handling quality decisions

- Use centralized exception handlers to normalize application errors.
- Keep domain/application exceptions separate from HTTP-specific `HTTPException`.
- Normalize validation, database, external-service, and unexpected errors into stable API contracts.
- Error codes are machine-readable API contracts; human messages are not.
- Never leak stack traces, SQL, provider errors, secrets, or internal paths.
- Preserve protocol-required headers such as `WWW-Authenticate` and `Retry-After`.
- Log unexpected errors once with request/trace correlation.

## SQLAlchemy session decisions

- Session lifecycle is owned externally by the service/unit-of-work boundary; repositories receive sessions.
- FastAPI `yield` dependencies are the standard request-scoped resource boundary.
- Do not create or commit sessions inside generic repository methods.
- Keep session lifecycle separate from business transaction boundaries.
- Do not share one `AsyncSession` across concurrent asyncio tasks.
- Be deliberate about `expire_on_commit`; async API serialization should not accidentally trigger hidden DB I/O.
- Do not pass request-scoped sessions into durable background jobs.
- Avoid lazy-loading/N+1 behavior during response serialization.

## Middleware quality decisions

- Use middleware for cross-cutting transport/observability concerns, dependencies for endpoint-specific policy, and services for business logic.
- Keep middleware instances stateless.
- Use FastAPI `yield` dependency scope deliberately; understand `request` vs `function` cleanup timing.
- Do not pass request-scoped resources into background tasks.
- Prefer pure ASGI middleware when `contextvars` propagation matters; Starlette documents `BaseHTTPMiddleware` limitations.
- Avoid buffering request/response bodies in middleware.
- Review middleware ordering whenever adding a new global concern.

## Migration quality decisions

- Alembic autogenerate output is a candidate draft and must be reviewed manually.
- Run `alembic check` in CI to detect model/schema drift.
- Use expand-and-contract for breaking schema changes under rolling deployment.
- Review destructive migrations, large indexes, type changes, and backfills for lock/data-loss risk.
- Separate large data backfills from ordinary schema migrations when appropriate.
- Prefer a controlled migration deployment job instead of running migrations from every API worker.
- Validate migrations against PostgreSQL, not only SQLite.

## Deployment topology decisions

- Local development is production-shaped, not production-sized.
- Distinguish worker count from replica count.
- Assume multiple workers/replicas when designing shared-state correctness.
- Size DB pools using worker × replica connection budgets.
- Use readiness for traffic routing and liveness for process health.
- Do not use sticky sessions to compensate for process-local state.
- Keep uploads/durable files outside replica-local filesystems.
- Long-lived SSE/WebSocket connections require explicit proxy/load-balancer timeout and multi-replica considerations.
- Separate API worker scaling from background worker scaling.

## Observability quality decisions

- Treat logs, metrics, and traces as separate but correlated signals.
- Use structured logs with stable fields.
- Keep request IDs and trace IDs conceptually distinct.
- Avoid secrets/PII and high-cardinality metric labels.
- Use OpenTelemetry for production traces/metrics where appropriate; OTel Python currently lists traces/metrics as stable and logs as development-status.
- Prefer OTLP/vendor-neutral exporters with environment-driven configuration.
- Console exporters are useful for local instrumentation.
- Use latency histograms/percentiles rather than averages alone.

## Phase 1 decisions

- API endpoints are organized with APIRouter/domain modules and an explicit API version boundary.
- Operation IDs are treated as stable API/client-generation contracts when generated clients are used.
- Input validation uses typed/bounded FastAPI/Pydantic parameters and models; resource limits are separate from structural validation.
- Persisted instants use timezone-aware UTC datetimes; business-local schedules retain IANA timezone identifiers.
- Outbound HTTP uses shared HTTPX AsyncClient instances with explicit connect/read/write/pool timeouts and connection limits.
- HTTPX TLS verification remains enabled outside deliberate local certificate testing.
- External HTTP responses are validated as untrusted data before entering domain logic.
- OpenAPI is treated as a generated contract artifact and release check, not optional documentation.

## Phase 2 database quality decisions

- PostgreSQL is the correctness/performance reference database.
- Transaction boundaries represent business units of atomic work.
- Choose isolation levels deliberately; default Read Committed is not a universal correctness solution.
- Use atomic updates, row locks, optimistic versioning, or stronger isolation according to the invariant.
- Do not use process-local locks for distributed correctness.
- Treat SQLAlchemy version counters as ORM flush behavior, not a replacement for database concurrency control or a safeguard for bulk updates.
- Use `EXPLAIN`/`EXPLAIN ANALYZE` to investigate real query plans.
- Avoid N+1, unbounded result loads, accidental lazy I/O, and Python-side filtering of large datasets.
- Use PostgreSQL-native UUID/JSONB/ARRAY/partial/expression indexes and ON CONFLICT/RETURNING deliberately when they improve correctness or performance.
- Verify indexes and PostgreSQL-specific choices against real workload data before production.

## Phase 3 decisions

- Non-idempotent mutations need explicit idempotency when retries can duplicate side effects.
- Same idempotency key + same request fingerprint replays the stored result; same key + different request is a conflict.
- Durable idempotency state belongs in shared storage and should use database uniqueness/concurrency controls.
- FastAPI BackgroundTasks is for small same-process follow-up work; durable/long-running work belongs in a queue/worker system.
- Use an outbox or equivalent strategy when DB commit and queue publication must remain consistent.
- Own application-wide DB/Redis/HTTP clients through FastAPI lifespan; request-scoped sessions belong to request/task boundaries.
- Use shared HTTPX clients with bounded timeouts, bounded retries, and idempotency-aware retry rules.
- StreamingResponse, SSE, and WebSockets are communication mechanisms, not durable job execution.
- Long-lived connections require disconnect handling, backpressure, proxy timeout review, and multi-replica event distribution.


## Phase 4 security hardening decisions

- Every client-controlled object identifier requires object-level authorization; do not rely on ID equality alone.
- Explicit Pydantic request/response schemas are security boundaries against mass assignment and excessive data exposure.
- Function-level/admin authorization must be explicit.
- Cookie-authenticated browser state changes require an explicit CSRF strategy; CORS alone is not CSRF protection.
- SSRF-sensitive outbound requests use an allowlist where possible, strict schemes/ports, private-IP/metadata protection, disabled/revalidated redirects, and network egress controls.
- Secrets come through typed configuration and external secret injection in production; no secrets in logs/images/source.
- Maintain explicit API/version inventory and deprecation policy.
- Map new endpoints to relevant OWASP API Top 10 risks during review.

## Phase 5 storage decisions

- Treat uploaded files as untrusted input.
- Enforce extension allowlists, content validation, size limits, generated object keys, and authorization.
- Keep durable storage behind an ObjectStorage interface.
- Local filesystem storage is PARTIAL compatibility, not production-equivalent object storage.
- Use quarantine/scanning when the threat model requires it.
- Store object metadata and ownership in PostgreSQL.
- Prefer short-lived signed URLs for large private object transfers when appropriate.
- Treat presigned URLs as bearer capabilities and never log them.
- Use shared durable storage for multi-replica production; replica-local disk is only transient.
- Make quotas and object lifecycle cleanup concurrency-safe and explicit.

## Phase 6 testing decisions

- Use pytest as the standard framework with registered strict markers.
- Use fixtures for isolated, explicit setup/cleanup.
- Use FastAPI dependency overrides for deterministic endpoint tests.
- Use TestClient context managers when lifespan must run.
- Use AnyIO + HTTPX AsyncClient for async API tests; account for lifespan separately because ASGITransport does not trigger it automatically.
- Use PostgreSQL for integration tests of PostgreSQL behavior; SQLite is not proof of PostgreSQL semantics.
- Prefer real Redis for distributed rate-limit/cache/lock tests.
- Treat OpenAPI as a contract and test breaking changes.
- Security tests must include negative authorization/resource-isolation cases.
- Concurrency tests assert invariants, not scheduler order.
- Use E2E tests sparingly for complete workflows.
- Use coverage as a risk signal, not as proof of correctness.

## Phase 7 operational decisions

- Design graceful degradation explicitly for optional/non-critical dependencies.
- Use timeouts, bounded retries, bulkheads, and load shedding before relying on circuit breakers.
- Circuit breakers should have explicit states, thresholds, cool-down, probe policy, and metrics.
- Define SLOs from user-visible SLIs; use error budgets to guide release/reliability decisions.
- Prefer actionable SLO burn/saturation alerts over paging on every low-level event.
- Treat application rollback and database rollback as separate decisions; prefer forward-fix when schema rollback is unsafe.
- Use staged/canary rollout where platform support and risk justify it.
- Define RPO/RTO from business requirements, not arbitrary engineering defaults.
- PostgreSQL recovery planning may require base backups plus continuous WAL/PITR; restore tests are mandatory evidence of recovery capability.
- Critical production behavior should have an operational runbook with symptoms, mitigation, recovery, escalation, and verification.

## Final audit decisions

- `SKILL.md` is the authoritative routing index and must reference only existing files.
- Shared policy files must have an explicit purpose/goal and substantive implementation rules.
- Local/prod files should describe environment-specific behavior without duplicating shared business rules.
- Portable skill files must not contain internal chat citation markup; use durable source URLs/Source sections instead.
- Before packaging, run every phase verifier plus `requirements/content_quality_audit.py`.
- Do not create a release ZIP until all gates pass.

## Final consistency audit state

- The authoritative skill tree is audited file-by-file before packaging; the current release count is recorded by the verification scripts rather than hard-coded here.
- Do not hard-code release file counts in memory; derive them from the current filesystem/audit.
- `SKILL.md` references are verified to resolve before packaging.
- Shared policy files are required to pass the structural quality gate before packaging.
- No internal/non-portable citation markup remains in the Markdown skill files.
- No zero-byte files are present.
- No known temporary security/audit artifact remains.
- `content_quality_audit.py` passes.
- `content_consistency_audit.py` passes.
- Phase 1 through Phase 7 verification scripts pass.
- Package only after all gates pass and `unzip -t` succeeds.

## Phase 8 decisions (external audit + new capability additions)

- Server-side `onupdate`/`server_default` columns need `eager_defaults=True` under async SQLAlchemy — `expire_on_commit=False` alone does not prevent `MissingGreenlet` on those specific columns.
- Custom FastAPI dependency functions needing `Request`/`BackgroundTasks` must type-annotate the parameter — an untyped `request` silently becomes a required query parameter, not a startup error.
- Login rate limiting needs two separate buckets (per-IP, per-username), never one combined key — a combined key lets one IP exhaust unlimited usernames (credential stuffing) before either limit fires.
- A global, unkeyed aggregate circuit breaker is required on auth endpoints in addition to per-key limits — distributed attacks across many IPs, each under its own per-key threshold, are invisible to keyed limiting by construction.
- Account-takeover response requires a `token_version`/security-stamp claim checked on every access and refresh — an `is_active` flag cannot invalidate specific already-issued sessions without disabling the whole account.
- Row-Level Security provides zero protection if the application's DB role is a superuser or has `BYPASSRLS` — verified directly; this is silent, with no error and no visible misconfiguration.
- PostgreSQL `current_setting('app.tenant')` (no `missing_ok`) fails loudly on an unset tenant context; the `missing_ok=true` variant fails silently (zero rows) — prefer the loud form so a missing `SET` is never mistaken for a legitimately empty result.
- Multi-tenant isolation, PII-at-rest (`pgcrypto`), and audit logging (`pgAudit`) are documented as distinct concerns from user-level authorization/secrets — do not conflate them.
- The transactional outbox pattern requires `FOR UPDATE SKIP LOCKED` the moment more than one relay worker runs, or concurrent workers double-publish the same event.
- Load testing an auth-adjacent endpoint must use one account per virtual user, not one shared login — a shared login collides with per-username rate limiting and produces false failures indistinguishable from a real capacity problem.
- WebSocket auth for bearer-JWT APIs (no cookie) uses first-message auth, not a query-string token; the server must send an explicit readiness ack after any async subscribe step, or a client-triggered event immediately after connecting can race the subscription and be silently dropped.
- A `pubsub.listen()`-only forwarding loop cannot detect a WebSocket disconnect with no new pub/sub traffic — pair it with a concurrent task whose only job is watching for the disconnect, race the two, and clean up in `finally`.
- CI/CD, an observability backend, multi-tenancy, PII protection, audit logging, the transactional outbox, load testing, feature flags, and TLS provisioning are now covered (`deployment/cicd.shared.md`, `observability/local_dev.md`+`prod.md`, `database/multi_tenancy.shared.md`, `security/pii_protection.shared.md`, `security/audit_logging.shared.md`, `async/outbox.shared.md`, `testing/load.shared.md`, `deployment/feature_flags.shared.md`, `networking/prod.md`).
- A project-scoping gate (`checklists/project-scoping.md`) runs before greenfield implementation — prefers the external `grill-me`/`grilling` plugin if installed, with a minimal fallback question set if not; the interview mechanism itself is deliberately not vendored into this skill.
- A sibling skill, `frontend-api-client`, generates a typed client + Zod runtime validators from this skill's own OpenAPI schema rather than hand-documenting the response contract — closes the loop on `api/response_format.shared.md` vs `api/response_contracts.shared.md`'s bare-vs-enveloped ambiguity, since the frontend never hardcodes either shape.
