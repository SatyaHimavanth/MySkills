# OWASP API Security Coverage — Shared

## Purpose

Provide an explicit checklist mapping the backend skill to the OWASP API Security Top 10 2023.

OWASP's current API Security Top 10 lists ten API-specific risks. The skill should not assume general authentication alone covers them.

## API1 — Broken Object Level Authorization

Covered by:

```text
security/object_authorization.shared.md
```

Required check:

```text
Every client-controlled object identifier → object-level authorization
```

## API2 — Broken Authentication

Covered by:

```text
security/authentication.shared.md
security/passwords.shared.md
```

## API3 — Broken Object Property Level Authorization

Covered by:

```text
security/object_authorization.shared.md
api/response_contracts.shared.md
api/schemas.shared.md
```

Response schemas and explicit update models are security boundaries.

## API4 — Unrestricted Resource Consumption

Covered by:

```text
api/resource_limits.shared.md
security/ratelimiting.shared.md
storage/shared.md
```

Controls include:

- request size limits
- list/page limits
- file limits
- timeouts
- rate limits
- concurrency limits
- downstream quotas

OWASP identifies bandwidth, CPU, memory, storage, and paid third-party calls as resources that APIs must control.

## API5 — Broken Function Level Authorization

Covered by:

```text
security/authorization.shared.md
```

Administrative/internal functions require explicit policy checks.

## API6 — Unrestricted Access to Sensitive Business Flows

Covered by:

```text
security/ratelimiting.shared.md
async/idempotency.shared.md
```

Business flows need abuse controls beyond generic authentication.

## API7 — Server Side Request Forgery

Covered by:

```text
security/ssrf.shared.md
```

## API8 — Security Misconfiguration

Covered by:

```text
security/http_security.shared.md
security/secrets.shared.md
configuration/shared.md
```

## API9 — Improper Inventory Management

Covered by:

```text
api/endpoints.shared.md
api/versioning.shared.md
```

Maintain endpoint/version inventory and explicitly deprecate/remove old surfaces.

## API10 — Unsafe Consumption of APIs

Covered by:

```text
http_client/shared.md
security/ssrf.shared.md
```

Validate third-party responses rather than trusting them as privileged input. OWASP explicitly calls out weaker security assumptions around integrated APIs.

## Security review requirement

Every new endpoint should identify which OWASP risks are relevant and which controls apply.

Do not write “OWASP compliant” as a substitute for evidence.

## Sources

- https://owasp.org/API-Security/editions/2023/en/0x11-t10/

