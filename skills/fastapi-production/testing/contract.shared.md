# Contract Testing — Shared

## Purpose

Prevent accidental API contract drift.

## OpenAPI as a contract

The generated OpenAPI document should be treated as a build artifact and compatibility surface.

Check important changes to:

- paths
- methods
- request schemas
- response schemas
- status codes
- required fields
- enum values
- authentication/security requirements
- deprecation metadata

## Breaking changes

Potentially breaking:

- removing a route
- changing an HTTP method
- changing success status codes
- making a field required
- changing field type
- removing a response field used by clients
- changing error codes
- changing pagination contract
- removing scopes

Additive changes are not automatically safe when clients reject unknown fields or when validation is strict; review client compatibility.

## Consumer contracts

If the project has external consumers, consider generated client tests or consumer-driven contracts instead of relying only on server-side endpoint tests.

## Snapshot caution

Snapshots can help detect OpenAPI drift, but do not blindly approve large snapshot changes. Review semantic API changes.
