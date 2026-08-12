# HTTP Security Configuration — Shared

## Purpose

Define safe HTTP behavior around hosts, HTTPS, proxy headers, CORS, security headers, and request limits.

## Trusted proxy boundary

Forwarded headers such as `X-Forwarded-For`, `X-Forwarded-Proto`, and `X-Forwarded-Host` are only trustworthy when they come through a configured trusted proxy boundary.

Never let arbitrary clients decide their source IP or public scheme by sending those headers directly.

## Host validation

Use host validation where the deployment requires it. Starlette provides `TrustedHostMiddleware` for validating the HTTP `Host` header.

## HTTPS

Use HTTPS in production. If TLS terminates at a trusted reverse proxy, configure the application to understand the forwarded scheme correctly.

Do not build security decisions around an untrusted forwarded scheme.

## CORS

CORS controls which browser origins may read responses. It is not authentication and it is not CSRF protection.

Use explicit allowed origins and decide credentials/methods/headers intentionally.

## Security headers

Apply headers appropriate to the application and deployment. For JSON APIs, avoid copying browser-application headers blindly; use the minimum necessary policy.

## Request/resource limits

Coordinate:

```text
proxy body limit
API body limit
endpoint validation
upload limit
```

The smallest limit in the path wins.

## Debug exposure

Do not expose debug traceback responses, interactive docs, or internal endpoints publicly unless explicitly approved by deployment policy.

## Security configuration review

Before production, verify:

- allowed hosts
- HTTPS behavior
- trusted proxy IPs
- CORS origins
- credential policy
- request limits
- debug disabled
- documentation exposure policy
- security headers
- secret source

## Forbidden

- wildcard CORS with credentials
- trusting arbitrary forwarded headers
- relying on CORS as authorization
- public debug mode
- exposing internal admin/debug routes by obscurity
