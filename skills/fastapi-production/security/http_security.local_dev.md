# HTTP Security — Local Development

## Purpose

Allow normal frontend development without teaching the application unsafe production assumptions.

## Rules

- Explicitly allow only the local frontend origins actually used, for example `http://localhost:5173`.
- Do not use wildcard CORS with credentialed browser sessions.
- Local HTTP may be acceptable when TLS is not part of the feature being tested.
- If cookie/security behavior is being tested, use a trustworthy HTTPS local setup.
- Document whether a reverse proxy is present.
- Do not trust arbitrary X-Forwarded-* headers from direct clients.

## Example

```python
allow_origins=["http://localhost:5173"]
allow_credentials=True
```

This configuration must not be copied to production without reviewing the actual public origins.
