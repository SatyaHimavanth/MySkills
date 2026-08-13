# HTTP Security — Local Development

## Purpose

Allow normal frontend development without teaching the application unsafe production assumptions.

## Rules

- Explicitly allow only the local frontend origins actually used, for example `http://localhost:5173`.
- Do not use wildcard CORS with credentialed browser sessions.
- Local HTTP may be acceptable when TLS is not part of the feature being tested.
- If cookie/security behavior is being tested, use a trustworthy HTTPS local setup: [mkcert](https://github.com/FiloSottile/mkcert) generates a local CA and locally-trusted certs (`mkcert -install && mkcert localhost 127.0.0.1`) — no browser warnings, closer to prod TLS behavior than a self-signed cert. Never commit the generated `rootCA-key.pem`; it can intercept any TLS traffic trusted by that machine.
- Document whether a reverse proxy is present.
- Do not trust arbitrary X-Forwarded-* headers from direct clients.

## Example

```python
allow_origins=["http://localhost:5173"]
allow_credentials=True
```

This configuration must not be copied to production without reviewing the actual public origins.
