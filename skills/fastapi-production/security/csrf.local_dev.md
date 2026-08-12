# CSRF — Local Development

## Purpose

Validate browser CSRF behavior locally without weakening the production security model.

## Rules

- If using bearer Authorization headers, document why browser cookie CSRF protection is not the primary control.
- If using cookie authentication, use the same CSRF mechanism as production whenever practical.
- Use HTTPS/local trustworthy URLs when testing browser security behavior.
- Keep CORS and CSRF decisions separate.
- Test same-origin success, cross-origin rejection, invalid tokens, invalid Origin, and missing Fetch Metadata according to policy.

## Local example

```text
React/Vite → cookie session → CSRF header → FastAPI
```

## Development shortcut policy

Do not disable CSRF globally merely to make a development frontend work. If a temporary bypass is explicitly required for a throwaway sandbox, it must be environment-gated and impossible to activate in production configuration.

## Browser test matrix

Test with both same-origin and cross-origin requests, credentialed and non-credentialed browser modes, and verify the production policy is enforced rather than merely logged.
