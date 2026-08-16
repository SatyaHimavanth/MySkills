# Production Readiness Checklist

First confirm the scale tier (`architecture/scale_tiers.shared.md`). Tier 1 items below are required for any production launch, including a small-team/internal one. Tier 2 items are only required once the Tier 1 → Tier 2 escalation gate has actually been met — do not implement them speculatively.

## Tier 1 — small-team production (default; ~100–1,000 users, single region)

- [ ] PostgreSQL used unless explicitly overridden
- [ ] Pydantic Settings validated at startup
- [ ] Secrets are externalized
- [ ] Structured logging enabled
- [ ] Health/readiness endpoints present
- [ ] Timeouts and graceful shutdown configured
- [ ] 2+ replicas behind a single load balancer, with shared Redis for cache/session/rate-limit state (single-replica + in-memory state is not production-ready even at small scale — see `architecture/scale_tiers.shared.md`)
- [ ] Rate limiting reviewed — per-key AND global aggregate breaker on auth endpoints (`security/ratelimiting.shared.md`)
- [ ] Account-takeover session revocation in place (`token_version`, `security/authentication.shared.md`)
- [ ] TLS provisioning configured, same Caddyfile local/prod (`networking/prod.md`)
- [ ] CI/CD pre-merge gates configured (`deployment/cicd.shared.md`)
- [ ] Multi-tenant isolation reviewed if the project actually serves more than one org — the Tier 1 default is single-tenant, so this is usually N/A (`database/multi_tenancy.shared.md`); when it does apply, confirm RLS policy AND non-superuser DB role
- [ ] Audit logging configured if compliance requires it (`security/audit_logging.shared.md`)
- [ ] Load tested against production-shaped infra, not SQLite/mocks (`testing/load.shared.md`)
- [ ] Migrations applied and reviewed
- [ ] Tests pass in a production-compatible setup
- [ ] No hidden local-only assumptions remain
- [ ] Cloud provisioning (managed DB/cache, IAM, networking) handed off to the project's cloud-provider skill, scoped to Tier 1 requirements only

## Tier 2 — regional/global scale (only after an escalation trigger in `architecture/scale_tiers.shared.md`)

- [ ] Concrete escalation trigger documented (latency data, compliance/residency requirement, measured capacity ceiling, or named multi-region requirement from scoping)
- [ ] Multi-region database strategy applied (`database/multi_region.shared.md`) — read-after-write handling, replica lag, clock skew
- [ ] CDN/edge and anycast DNS introduced only for the specific asset/latency problem identified, not wholesale
- [ ] Connection multiplexing (PgBouncer/RDS Proxy) sized against the primary's real connection budget across all regions
- [ ] Cross-region trace correlation added if cross-region debugging is actually needed
