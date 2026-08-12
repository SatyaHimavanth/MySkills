# OpenAPI — Local Development

## Rules
- Keep docs enabled for ordinary local development unless the project intentionally disables them.
- Use the same route/version/security metadata as production.
- Inspect `/docs`, `/redoc`, and `/openapi.json` after API changes.
- Use local examples only; never insert real credentials.
- If a reverse proxy/path prefix is used, test the generated server URLs and documentation links through that proxy shape.

## Validation workflow
After adding or changing a route, inspect the generated schema and interactive documentation. Check that request fields, response fields, security requirements, examples, status codes, and deprecation metadata match the implementation.

## Proxy testing
If local development runs behind a reverse proxy or path prefix, test the externally visible URL rather than only the direct Uvicorn URL. Incorrect proxy metadata can make documentation links point to the wrong host or path.
