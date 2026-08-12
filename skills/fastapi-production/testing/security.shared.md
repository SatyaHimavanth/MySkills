# Security Testing — Shared

## Purpose

Verify that authentication, authorization, resource isolation, rate limits, CSRF defenses, and security error behavior fail closed where required.

## Authentication matrix

Test at least:

```text
no token
expired token
malformed token
wrong signature
wrong issuer/audience where applicable
disabled user
valid user
```

## Authorization matrix

For protected resources test:

```text
anonymous
same-user
other-user
same-tenant
cross-tenant
admin
insufficient-scope
```

The same endpoint must not merely be tested with an administrator.

## BOLA/property authorization

Test that changing an object ID in the URL cannot access another user's/tenant's resource.

Test that request models cannot mass-assign protected fields such as:

```text
owner_id
tenant_id
is_admin
permissions
security state
```

unless explicitly authorized.

## Rate-limit tests

Test:

- under limit
- boundary
- rejected request
- reset/expiry
- independent principals
- backend failure policy
- multiple workers when distributed behavior matters

## CSRF tests

For cookie-authenticated browser flows test:

- missing CSRF token
- invalid token
- wrong Origin/Referer where enforced
- safe methods
- login CSRF controls where applicable

Do not confuse bearer-token header auth with cookie-auth CSRF requirements.

## SSRF tests

Test blocked destinations:

```text
localhost
127.0.0.1
::1
private IPv4 ranges
link-local
cloud metadata endpoint
blocked ports/schemes
redirect to blocked destination
```

Use safe fixtures and controlled test endpoints; never probe real cloud metadata during tests.

## Secrets

Tests must fail if sensitive values appear in logs or error responses where such checks are practical.
