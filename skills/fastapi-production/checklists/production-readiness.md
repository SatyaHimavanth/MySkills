# Production Readiness Checklist

- [ ] PostgreSQL used unless explicitly overridden
- [ ] Pydantic Settings validated at startup
- [ ] Secrets are externalized
- [ ] Structured logging enabled
- [ ] Health/readiness endpoints present
- [ ] Timeouts and graceful shutdown configured
- [ ] Rate limiting reviewed — per-key AND global aggregate breaker on auth endpoints (`security/ratelimiting.shared.md`)
- [ ] Account-takeover session revocation in place (`token_version`, `security/authentication.shared.md`)
- [ ] TLS provisioning configured, same Caddyfile local/prod (`networking/prod.md`)
- [ ] CI/CD pre-merge gates configured (`deployment/cicd.shared.md`)
- [ ] Multi-tenant isolation reviewed if applicable — RLS policy AND confirmed non-superuser DB role (`database/multi_tenancy.shared.md`)
- [ ] Audit logging configured if compliance requires it (`security/audit_logging.shared.md`)
- [ ] Load tested against production-shaped infra, not SQLite/mocks (`testing/load.shared.md`)
- [ ] Migrations applied and reviewed
- [ ] Tests pass in a production-compatible setup
- [ ] No hidden local-only assumptions remain
