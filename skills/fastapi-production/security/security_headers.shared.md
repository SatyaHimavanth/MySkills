# Security Headers — Shared

## Purpose

Define HTTP response-header policy appropriate to the application's browser and API exposure to defend against clickjacking, MIME sniffing, and cross-site scripting (XSS).

## Rules

- Enforce standard security headers on production API and web responses.
- Use `Strict-Transport-Security` (HSTS) when HTTPS is active in production.
- Use `X-Content-Type-Options: nosniff` to prevent MIME-type sniffing.
- Use `X-Frame-Options: DENY` (or `SAMEORIGIN`) to prevent framing and clickjacking attacks.
- Use `Referrer-Policy: strict-origin-when-cross-origin` to restrict sensitive URL leakage in HTTP referrers.
- Apply `Permissions-Policy` to disable unused browser features (geolocation, camera, microphone).
- Set `Content-Security-Policy` for any endpoint serving HTML — this is the primary XSS mitigation the other headers don't cover. Start with `default-src 'self'` and tighten per-app; a missing CSP leaves the file's stated XSS goal unaddressed.

## Production Security Headers Middleware Pattern

```python
from starlette.types import ASGIApp, Receive, Scope, Send

class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp, is_production: bool = True):
        self.app = app
        self.is_production = is_production

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message: dict) -> None:
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                
                # Default API security headers
                headers[b"x-content-type-options"] = b"nosniff"
                headers[b"x-frame-options"] = b"DENY"
                headers[b"referrer-policy"] = b"strict-origin-when-cross-origin"
                headers[b"permissions-policy"] = b"geolocation=(), camera=(), microphone=()"

                if self.is_production:
                    # Enforce HTTPS for 1 year including subdomains
                    headers[b"strict-transport-security"] = b"max-age=31536000; includeSubDomains"

                message["headers"] = list(headers.items())
            await send(message)

        await self.app(scope, receive, send_with_headers)
```

## HSTS Caution

Only enable HSTS when HTTPS is reliably deployed across all subdomains; HSTS instructs browsers to refuse HTTP connections for the duration of `max-age`.

## Forbidden

- HSTS header injected on unencrypted plain HTTP connections
- using security headers as a replacement for proper authentication or input validation
