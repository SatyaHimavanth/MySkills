# Production Readiness Checklist

- [ ] PostgreSQL used unless explicitly overridden
- [ ] Pydantic Settings validated at startup
- [ ] Secrets are externalized
- [ ] Structured logging enabled
- [ ] Health/readiness endpoints present
- [ ] Timeouts and graceful shutdown configured
- [ ] Rate limiting reviewed
- [ ] Migrations applied and reviewed
- [ ] Tests pass in a production-compatible setup
- [ ] No hidden local-only assumptions remain
