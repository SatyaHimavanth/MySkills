# Security Headers — Local Development

## Purpose

Keep useful browser-facing security protections without creating development lockouts or misleading production assumptions.

## Rules

- Keep `X-Content-Type-Options: nosniff` where useful.
- Do not enable production HSTS for a development hostname unless the developer understands the browser impact.
- Keep CORS, proxy trust, and security headers as separate policies.
- Test CSP only where browser-rendered content actually exists.

## Forbidden

- copying a production CSP blindly into a frontend development environment
- enabling HSTS without understanding its host scope
