# HTTP Security — Production

## Rules

- Enforce HTTPS at the public edge.
- Configure trusted proxy IPs explicitly.
- Use `TrustedHostMiddleware` when the deployment has a finite host allowlist.
- Use explicit CORS origins and credential policy.
- Keep debug/interactive internals disabled or isolated according to deployment policy.
- Coordinate reverse-proxy and application request-size/timeouts.
- Use appropriate security headers.

## Public topology

```text
Internet
  ↓
TLS/WAF/proxy
  ↓
load balancer
  ↓
FastAPI
```

The application must know which headers are trusted from this chain.

## Verification

Test:

- HTTP → HTTPS behavior
- allowed and disallowed Host values
- trusted and untrusted forwarded headers
- CORS preflight
- credentialed CORS
- oversized requests
- public debug/docs policy
