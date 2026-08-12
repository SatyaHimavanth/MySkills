# Object, Property, and Function Authorization — Shared

## Purpose

Prevent authorization bypasses at the object, property, and function levels.

OWASP API1 requires object-level authorization checks for every endpoint that accesses an object using a client-supplied identifier. API3 covers property-level exposure/mass assignment, and API5 covers function-level authorization.

## Object-level authorization (BOLA)

Every endpoint using a client-supplied identifier must answer:

```text
Who is requesting?
What object is being accessed?
What action is requested?
Is this principal allowed to perform this action on THIS object?
```

Bad:

```python
user_id = path_user_id
return await repo.get_user(user_id)
```

when authentication alone does not prove access.

Better:

```python
user = await repo.get_user_for_principal(
    user_id=user_id,
    principal=current_user,
)
```

or perform an explicit policy check before the operation.

Do not rely only on matching `current_user.id == path_user_id`; many domains use tenant ownership, membership, roles, delegation, or resource relationships. OWASP explicitly notes that this simple comparison is insufficient for general BOLA prevention.

## Query-level authorization

Prefer pushing access boundaries into the database query where it reduces TOCTOU risk.

Example:

```python
stmt = (
    select(Document)
    .where(
        Document.id == document_id,
        Document.tenant_id == current_user.tenant_id,
    )
)
```

Then apply action-specific policy as needed.

## Property-level authorization

Do not expose every field of a domain object.

Use dedicated Pydantic schemas:

```text
DocumentResponse
DocumentAdminResponse
DocumentUpdateRequest
DocumentAdminUpdateRequest
```

Do not accept arbitrary update dictionaries:

```python
setattr(document, key, value)
```

Allow only explicitly writable fields.

OWASP API3 specifically recommends schema-based response validation and avoiding generic object serialization/mass assignment.

## Function-level authorization

Administrative functions require explicit authorization.

Examples:

```text
POST /api/v1/admin/users/{id}/disable
POST /api/v1/jobs/{id}/retry
GET  /api/v1/internal/metrics
```

Do not rely on obscurity or a hidden route prefix.

Use explicit permission policies/dependencies.

## Tenant boundaries

For multi-tenant applications, tenant identity must be established server-side.

Do not trust:

```json
{"tenant_id": "client-selected-tenant"}
```

as authorization proof.

Derive the current tenant from authenticated identity, authorized membership, or an approved server-side context.

## Resource hierarchy

For nested resources:

```text
GET /tenants/{tenant_id}/documents/{document_id}
```

validate the complete relationship:

```text
tenant accessible?
        ↓
document belongs to tenant?
        ↓
principal has document permission?
```

Do not only check the final ID.

## Property update policy

For each update schema define:

```text
readable fields
writable fields
server-managed fields
admin-only fields
immutable fields
```

Example:

```python
class UserUpdateRequest(BaseModel):
    display_name: str | None
```

Do not allow:

```text
is_admin
password_hash
tenant_id
account_status
```

unless the endpoint explicitly represents that privileged operation.

## Authorization tests

For every protected resource operation test:

- authenticated owner allowed
- authenticated non-owner denied
- correct tenant allowed
- cross-tenant denied
- privileged role allowed only where intended
- missing scope denied
- disabled account denied
- object not found behavior does not leak sensitive existence information

## Forbidden patterns

- ID-only authorization
- trusting client tenant IDs
- generic mass assignment
- serializing full ORM objects
- hiding admin endpoints instead of protecting them
- frontend-only authorization
- copying an authorization check from one endpoint without verifying the domain rule

## Sources

- https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
- https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/

