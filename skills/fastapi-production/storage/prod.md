# File Storage — Production

## Purpose

Keep durable files independent of API replicas and protect private objects.

## Recommended architecture

```text
client
  ↓
FastAPI
  ↓
authorize
  ↓
ObjectStorage interface
  ↓
S3-compatible/cloud object storage
```

PostgreSQL stores metadata and object references.

## Direct upload

Prefer direct-to-object-storage upload for large files when the provider and threat model support it:

```text
client
  ↓
FastAPI upload-init endpoint
  ↓
authorize + reserve quota + create pending object
  ↓
short-lived signed upload URL
  ↓
client → object storage
  ↓
verification/finalization
  ↓
accepted object
```

AWS documents presigned URLs as time-limited bearer capabilities whose permissions are constrained by the signing principal and requested operation. [Certain]

## Private downloads

Preferred pattern:

```text
GET /objects/{id}/download
  ↓
authentication
  ↓
authorization
  ↓
short-lived signed GET URL
```

Do not return permanent public storage URLs for private data.

## Quotas

Maintain quota state in durable/shared storage.

For example:

```text
tenant_storage_used
pending_bytes
maximum_bytes
```

Update quota atomically with object state where correctness requires it.

## Scanning

If scanning is required:

```text
PENDING_SCAN
      ↓
scanner worker
   ├── REJECTED
   └── ACCEPTED
```

Only accepted objects become accessible to normal users.

## Object lifecycle

Define cleanup for:

- abandoned pending uploads
- rejected/quarantined files
- expired objects
- deleted metadata
- failed background processing

Use scheduled cleanup jobs rather than relying only on application startup.

## Multi-replica rule

Never use local disk as the durable source of truth for user files when more than one API instance can handle requests.

Local temp files are acceptable for transient processing when the workflow explicitly manages cleanup.

## Signed URL policy

Define an upper bound for signed URL lifetime.

Avoid logging complete presigned URLs because the URL itself is a bearer capability.

## Production checklist

- [ ] storage provider configured through typed settings
- [ ] object access authorized
- [ ] object keys server-generated
- [ ] size limits enforced
- [ ] quota policy implemented
- [ ] scanning policy defined when required
- [ ] private objects remain private
- [ ] signed URLs expire
- [ ] abandoned objects cleaned up
- [ ] API replicas do not depend on local durable disk
