# Authentication — Local Development

## Goal

Keep local authentication protocol-compatible with production while allowing developer-only credentials and local identity infrastructure.

## Rules

- Use the same token format, claims, request/response schemas, and authorization model as production whenever possible.
- Use development-only signing secrets.
- Never use production identities, tokens, refresh tokens, or secrets.
- Keep authentication enabled by default.
- A deliberately unauthenticated sandbox must be explicit, isolated, and impossible to select accidentally in production.
- Test expired, malformed, invalid-signature, insufficient-scope, disabled-user, and revoked-session cases locally.

## Application-owned local flow

```text
PostgreSQL user
    ↓
pwdlib/Argon2 verification
    ↓
PyJWT token
    ↓
OAuth2PasswordBearer
    ↓
current-user dependency
    ↓
authorization
```

## External identity provider

If production uses OIDC/OAuth2, prefer the provider's test tenant or documented local/test mode. Do not invent an unrelated fake token scheme.

## Local settings

Keep auth configuration in Pydantic Settings:

```env
APP_AUTH__JWT_SECRET=development-only-secret-please-change-32bytes-min
APP_AUTH__ACCESS_TOKEN_EXPIRE_MINUTES=15
```

Verified: PyJWT raises `InsecureKeyLengthWarning` for HMAC (`HS256`) secrets under 32 bytes — a shorter placeholder like `development-only-secret` (23 bytes) triggers this on every token issuance. It's a real, if low-severity, signal worth keeping clean even in local dev: a placeholder that trips a security warning trains developers to ignore that warning class by the time it matters in a real secret. Pick a local placeholder that's at least 32 bytes.

## Forbidden

- production secrets locally
- production user databases locally
- authentication bypass as a permanent default
- a local token format incompatible with production
- an HMAC JWT secret (local or production) under 32 bytes
