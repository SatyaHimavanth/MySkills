# CORS — Production

## Purpose

Limit browser cross-origin access to explicitly approved origins while preserving the chosen authentication model.

## Rules

- Use an explicit allowlist of approved browser origins.
- Review credentials, methods, and headers together.
- Do not use `*` with credentialed browser access.
- Do not broaden CORS to fix an unrelated authentication, proxy, or CSRF problem.
- Test preflight and credentialed requests during deployment validation.

## Forbidden

- reflecting arbitrary `Origin` values into `Access-Control-Allow-Origin`
- treating CORS as authentication or CSRF protection
