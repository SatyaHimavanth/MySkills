# Phase 4 Coverage Matrix

| Requirement | File(s) | Shared | Local | Prod | Verification | Status |
|---|---|---:|---:|---:|---|---|
| BOLA / object authorization | security/object_authorization.shared.md | ✓ | via tests | via policy | policy sections | COMPLETE |
| Property-level authorization / mass assignment | security/object_authorization.shared.md | ✓ | via tests | via policy | schema/update rules | COMPLETE |
| Function-level authorization | security/object_authorization.shared.md, security/authorization.shared.md | ✓ | — | — | policy sections | COMPLETE |
| SSRF | security/ssrf.shared.md | ✓ | — | — | URL/DNS/redirect/egress sections | COMPLETE |
| CSRF | security/csrf.shared.md, security/csrf.local_dev.md, security/csrf.prod.md | ✓ | ✓ | ✓ | cookie/origin/Fetch Metadata sections | COMPLETE |
| Secrets management | security/secrets.shared.md | ✓ | via configuration | ✓ | source/rotation/logging sections | COMPLETE |
| OWASP API4 resource consumption | api/resource_limits.shared.md, security/ratelimiting.shared.md | ✓ | ✓ | ✓ | bounds/fanout/timeout sections | COMPLETE |
| OWASP API8 security configuration | security/http_security.shared.md, security/secrets.shared.md | ✓ | ✓ | ✓ | configuration references | COMPLETE |
| OWASP API9 inventory/versioning | api/versioning.shared.md, api/endpoints.shared.md | ✓ | — | — | inventory/deprecation sections | COMPLETE |
| OWASP API10 unsafe API consumption | http/clients.shared.md, security/ssrf.shared.md | ✓ | via client policy | via client policy | response/transport validation | COMPLETE |
