# Authorization — Shared

## Purpose

Provide a centralized authorization model for route, scope, role, tenant, and resource decisions.

## Layers

```text
route access
  ↓
scope/permission
  ↓
role policy
  ↓
tenant/resource ownership
  ↓
action-specific rule
```

## Default deny

Protected functionality requires an explicit authorization decision.

## Scope checks

Use FastAPI `Security()` for OAuth2 scope requirements so the requirement appears in OpenAPI.

```python
@router.delete("/users/{user_id}")
async def delete_user(
    current_user: Annotated[
        User,
        Security(get_current_user, scopes=["users:delete"]),
    ],
    user_id: UUID,
):
    ...
```

## Roles vs permissions

Roles are coarse groups. Permissions/scopes represent capabilities. Resource-level checks determine whether the principal may act on a specific object.

Do not treat a role as proof of ownership.

## Centralization

Prefer reusable policies:

```text
require_scope()
require_admin()
require_tenant_access()
require_resource_access()
```

Keep authorization tests beside policy code and endpoint integration tests.

## Tenant security

Derive tenant identity from trusted server-side identity/membership. Never trust a client-selected tenant ID as proof of authorization.

## Testing

Cover:

- allowed principal
- missing scope
- insufficient role
- wrong tenant
- wrong owner
- disabled account
- unauthenticated request

## Forbidden

- frontend-only authorization
- ID equality as a universal authorization mechanism
- hiding admin routes instead of protecting them
- duplicated policy logic that can drift
