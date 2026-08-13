# Networking — Local Development

## Purpose

Keep local routing simple while making proxy-specific behavior explicit when it is tested.

## Rules

- Direct client-to-FastAPI development is acceptable.
- If a local reverse proxy is used, document its address and trust boundary.
- Test forwarded headers only through the configured proxy path.
- Do not make authorization/rate-limit decisions from arbitrary local `X-Forwarded-*` headers.
- Keep CORS origins explicit even in local development.

## Example

```text
browser → FastAPI
```

or, when proxy behavior is being tested:

```text
browser → local proxy → FastAPI
```

## Local HTTPS via Caddy (same Caddyfile as production)

If Caddy is the local reverse proxy, use the identical Caddyfile as production — see `networking/prod.md` — with `SITE_ADDRESS` unset (defaults to `localhost`). Caddy detects `localhost`/private IPs are not publicly issuable and automatically switches to its own internal CA instead of attempting Let's Encrypt — verified directly (`caddy run` against a bare `localhost` site block logs `enabling automatic TLS certificate management, domains: [localhost]` using its internal PKI, no ACME attempt). Run `caddy trust` once to install that CA into the local trust store, same effect as `mkcert -install`. No cert files, no toggle logic, no mkcert needed in this case — one Caddyfile genuinely works unmodified in both environments.

Only reach for `mkcert` (see `security/http_security.local_dev.md`) when there is no local Caddy/reverse-proxy in the loop — e.g. testing directly against `uvicorn --ssl-keyfile/--ssl-certfile`.
