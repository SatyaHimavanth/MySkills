# Networking and Proxy Routing — Shared

## Purpose

Define the trust boundary between clients, reverse proxies/load balancers, and FastAPI.

## Rules

- Treat forwarded headers as untrusted unless they originate from explicitly trusted proxies.
- Define the proxy chain before using client IP, scheme, or host headers for security decisions.
- Keep request IDs and trace context through proxies.
- Ensure proxy and application body-size/timeout limits are compatible.
- Do not use client-supplied `X-Forwarded-For` as an authenticated identity signal.

## Routing chain

```text
client
  ↓
WAF/CDN
  ↓
load balancer/reverse proxy
  ↓
FastAPI
```

## Security-sensitive values

Client IP, HTTPS scheme, host, and original port can influence rate limiting, redirects, URL generation, logging, and SSRF defenses. Only trust forwarded values inside the configured proxy boundary.
