# Secrets Management — Shared

## Purpose

Keep credentials and cryptographic material out of source code, logs, container images, and accidental API responses.

## Classification

Separate:

```text
configuration
secrets
public identifiers
```

Examples of secrets:

- JWT signing keys
- database passwords
- API keys
- OAuth client secrets
- object-storage credentials
- private keys
- webhook signing secrets

## Source policy

Use Pydantic Settings as the application boundary.

Local:

```text
.env / local secret source
```

Production:

```text
secret manager / deployment secret injection
```

Do not change application code when changing the secret source.

## Secret values in memory

Use `SecretStr`/equivalent typed handling where practical.

Do not log full secret values.

Be aware that once a secret is passed into a third-party library it may still exist in process memory; the skill should avoid promising memory-perfect erasure in Python.

## Rotation

Every important secret needs a rotation story:

```text
current secret
    ↓
introduce new secret
    ↓
roll/reload services
    ↓
verify
    ↓
retire old secret
```

For signing-key rotation, support overlapping verification keys when the token system requires it.

## Repository hygiene

Never commit:

```text
.env
private keys
production credentials
cloud credentials
real access tokens
```

Use `.env.example` with safe placeholders.

## Logs/telemetry

Never log secrets or authentication headers.

Redact sensitive fields in structured logging and error reporting.

## External API credentials

Give each integration its own credential where practical.

Avoid using one superuser API key for every external service.

## Runtime configuration

Secrets should be injectable without modifying the application image/source tree.

Production containers should not contain `.env` files copied during build.

## Failure behavior

Missing required production secrets should fail startup/readiness rather than silently using insecure defaults.

## Testing

Tests must use dedicated test credentials and must not contact production identity/storage/payment systems accidentally.

## Forbidden

- secrets in source code
- secrets in Git history
- printing Settings objects
- secrets in exception responses
- production secrets in local development
- one universal credential for unrelated external systems
- insecure fallback values for required production secrets
