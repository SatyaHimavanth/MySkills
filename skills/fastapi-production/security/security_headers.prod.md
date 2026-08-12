# Security Headers — Production

## Purpose

Apply browser-facing security headers appropriate to the application's content model and HTTPS deployment.

## Rules

- Enable HSTS only when production HTTPS is stable and the intended host scope is known.
- Apply `X-Content-Type-Options: nosniff` where appropriate.
- Use CSP for browser-rendered content where applicable; a JSON-only API does not automatically need a complex CSP.
- Review headers through automated HTTP tests.
- Keep header policy separate from CORS and proxy trust.

## Forbidden

- enabling headers without understanding their browser semantics
- assuming all browser security headers materially improve a JSON-only API
