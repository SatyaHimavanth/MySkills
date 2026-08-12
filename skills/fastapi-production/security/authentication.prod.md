# Authentication — Production

## Goal

Provide secure identity verification and session/token lifecycle in a multi-worker, multi-replica environment.

## Rules

- Use trusted production identity-provider configuration.
- Validate JWT signatures with an explicit algorithm allowlist.
- Validate `exp`; validate `iss`/`aud` when they are part of the provider contract.
- Keep access tokens short-lived.
- Use refresh/session lifecycle for long-lived sessions.
- Handle signing-key rotation where external identity providers rotate keys.
- Never log access tokens, refresh tokens, Authorization headers, passwords, or signing secrets.
- Keep authentication state that needs cross-replica consistency in shared durable storage.

## Readiness checks

Before the application is ready to receive traffic, validate required identity configuration, key material/provider reachability when required, and the user database dependency.

## Multi-replica state

Cross-replica authentication state may include:

- refresh-token revocation
- server-side sessions
- security-stamp/token-version changes
- account lockout state
- login abuse controls

Do not keep these only in process memory.

## Forbidden

- arbitrary token issuers
- unverified JWT claims
- local-memory sessions for durable authentication state
- multi-week access tokens used as a substitute for session design
