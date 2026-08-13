# Networking — Production

## Purpose

Define the trusted proxy and routing boundary for production FastAPI deployments.

## Rules

- Configure the exact trusted proxy/load-balancer addresses or trusted-hop model supported by the deployment.
- Validate HTTPS/host/forwarded-header behavior through deployment tests.
- Align body-size and timeout policies across WAF, proxy, load balancer, and FastAPI.
- Preserve request/trace IDs across the routing chain.
- Use readiness to decide whether an instance receives traffic.

## Forbidden

- trusting arbitrary `X-Forwarded-*` headers
- assuming the application sees the public client address without proxy configuration

## TLS certificate provisioning

Terminate TLS at the proxy (Caddy), not in FastAPI/uvicorn. **Do not** try to make one Caddyfile "interchangeable" by swapping literal cert file paths (e.g. mkcert's generated `.pem` files) in and out per environment — verified broken: a `tls {$VAR}` line with `$VAR` unset fails Caddyfile parsing outright (`wrong argument count or unexpected line ending after 'tls'`), it does not gracefully fall through to automatic HTTPS.

The verified, actually-interchangeable approach: omit the `tls` directive entirely and drive only the site address by environment variable. Caddy's automatic HTTPS already branches on the domain itself — no toggle needed:

```
# Caddyfile — identical file in local dev and production
{$SITE_ADDRESS:localhost} {
    bind 0.0.0.0
    reverse_proxy api:8000
}
```

```yaml
# docker-compose.yml (prod)
services:
  caddy:
    image: caddy:2
    ports: ["80:80", "443:443"]
    environment:
      SITE_ADDRESS: yourdomain.com
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
    depends_on: [api]
volumes:
  caddy_data:
```

- `SITE_ADDRESS` unset/`localhost` → Caddy uses its own internal CA (no ACME attempt) — see `networking/local_dev.md`.
- `SITE_ADDRESS=yourdomain.com` → Caddy automatically obtains and renews a Let's Encrypt certificate via ACME HTTP-01.

Prerequisites for the production case: DNS A record pointing at the server's public IP, and ports 80 (ACME challenge)/443 reachable from the internet.
