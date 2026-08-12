# API Versioning and Inventory — Shared

## Purpose

Keep the deployed API surface discoverable and prevent accidental breaking changes or forgotten legacy endpoints.

OWASP API9 identifies improper inventory management as an API-specific security risk.

## Versioning default

Prefer an explicit path version such as:

```text
/api/v1
```

unless the project already has a coherent alternative.

## Version boundaries

Keep version-specific routers/schemas isolated enough that a breaking change can be introduced without silently mutating an existing contract.

```text
api/v1/users.py
api/v2/users.py
```

Share service/domain behavior where safe; do not duplicate the whole business layer just to change a representation.

## Breaking changes

Treat these as potentially breaking:

- removed/renamed field
- changed type or nullability
- changed status code
- changed error code
- changed pagination semantics
- authentication scheme change
- authorization policy change

Prefer additive changes when possible.

## Deprecation

For deprecated endpoints:

- mark them deprecated in OpenAPI
- document replacement
- define removal date/condition
- monitor usage
- remove only after migration policy allows it

## Inventory

Maintain a discoverable inventory of:

```text
route
HTTP method
tags
version
auth requirement
owner/status
```

Internal/debug endpoints should not accidentally become public API surface.

## Docs

Generated OpenAPI should represent the intended public surface. Exclude or isolate internal tools according to project policy.

## Forbidden

- silent v1 contract breaks
- forgotten deprecated routes
- undocumented admin/internal endpoints
- multiple incompatible versioning schemes without an explicit reason

## Sources

- https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- https://fastapi.tiangolo.com/tutorial/metadata/

