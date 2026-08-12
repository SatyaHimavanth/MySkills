# OpenAPI — Production

## Rules
- Decide explicitly whether Swagger/ReDoc should be public, authenticated, or disabled.
- Keep the generated OpenAPI document versioned or otherwise reviewable when clients depend on it.
- Ensure proxy/path-prefix configuration produces correct documentation URLs.
- Do not expose internal/admin schemas unnecessarily.
- Review security schemes, routes, deprecated endpoints, and response contracts before release.

## Release review
Treat the OpenAPI diff as a release review artifact. Flag removed paths, changed required fields, changed enum values, changed response status codes, changed auth/security requirements, and operation-ID changes when generated clients depend on them.

## Documentation exposure
Documentation availability is a security/configuration decision. A public `/docs` or `/openapi.json` endpoint should be deliberate; otherwise protect or disable it according to the deployment policy.
