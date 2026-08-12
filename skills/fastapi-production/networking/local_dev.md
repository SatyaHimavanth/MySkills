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
