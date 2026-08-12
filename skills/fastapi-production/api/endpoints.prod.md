# Endpoint Management — Production

## Purpose
Keep the public API inventory, versioning, and routing stable across rolling deployments.

## Rules
- Inventory every deployed route and version.
- Keep deprecated routes documented until their removal window ends.
- Keep operation IDs stable when generated clients depend on them.
- Ensure old and new application versions can coexist during rolling deployments.
- Isolate admin/internal endpoints from public traffic and documentation as required.
- Keep health/readiness/metrics routes separate from business API routing.

## Forbidden
- silently replacing an endpoint with a breaking route
- exposing debug/admin routes publicly
- removing a version without an explicit migration policy
