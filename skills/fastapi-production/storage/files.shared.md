# File Handling and Upload Security — Shared

## Purpose

Define one safe file boundary for uploads, downloads, temporary processing, and object storage.

Uploaded files are untrusted input. OWASP recommends allowlisting required file types, validating content rather than trusting the `Content-Type` header, generating server-side filenames, limiting file size, and authorizing uploads. [Certain] 

FastAPI's `UploadFile` exposes uploaded file metadata and a file-like interface. Use it for normal multipart uploads instead of reading large files into `bytes` by default. [Certain]

## Upload decision flow

```text
HTTP request
   ↓
authentication
   ↓
authorization / tenant quota
   ↓
request/body size guard
   ↓
UploadFile
   ↓
extension allowlist
   ↓
content/signature validation
   ↓
size/checksum calculation
   ↓
quarantine storage
   ↓
malware/content scan if required
   ↓
accepted durable object
   ↓
metadata transaction
```

## Allowed file types

Create an allowlist based on business requirements.

Example:

```python
ALLOWED_TYPES = {
    "application/pdf": {".pdf"},
    "text/csv": {".csv"},
}
```

Do not accept arbitrary file types because the client happens to send them.

The extension is one signal, not proof of file type.

## Content-Type is untrusted

The client can spoof:

```http
Content-Type: application/pdf
```

Do not treat it as proof that the bytes are a PDF. OWASP explicitly warns that the header is user-controlled. [Certain]

For security-sensitive workflows combine:

```text
extension
Content-Type
magic/signature bytes
safe parser
```

## File size limits

Enforce limits at more than one layer when practical:

```text
proxy / gateway
   ↓
FastAPI request policy
   ↓
per-file limit
   ↓
per-tenant quota
   ↓
storage quota
```

Do not rely only on the application reading bytes and then deciding the file was too large.

The proxy and application limits must agree so one layer does not accept a payload another layer cannot handle.

## Multipart and memory usage

Prefer:

```python
async def upload(file: UploadFile):
    ...
```

over:

```python
async def upload(file: bytes):
    ...
```

for potentially large files.

Do not call `await file.read()` without a bounded-size strategy for large uploads.

For very large files, prefer direct object-storage uploads with a short-lived signed upload URL where appropriate.

## Server-generated object keys

Never use the client filename as the storage path.

Bad:

```python
Path(upload.filename)
```

Use an application-generated opaque key:

```text
tenant/{tenant_id}/objects/{object_id}
```

Keep the original filename as metadata if the application needs it.

## Path traversal

Never concatenate user input into a filesystem path.

Bad:

```python
path = upload_root / user_supplied_name
```

Even after filename sanitization, prefer generated storage keys so the path itself is not controlled by the client.

## Filename metadata

If retaining the original filename:

- enforce a maximum length
- store it as data, not a path
- normalize or reject unsafe control characters
- do not reflect it into HTTP headers without proper encoding

## Quotas

Define quotas separately from per-request limits:

```text
per-file limit
per-request total limit
per-user daily quota
per-tenant storage quota
per-job output quota
```

Quota updates must be concurrency-safe.

Do not implement:

```python
if used + size < quota:
    used += size
```

without a transaction/locking strategy.

## Quarantine

For untrusted files that require scanning or parsing:

```text
upload
  ↓
quarantine
  ↓
scan/validate
  ├── rejected
  └── accepted
       ↓
   durable object
```

Do not expose a file before it passes the required checks.

## Malware scanning

If the application's threat model requires malware scanning, define an adapter:

```python
class MalwareScanner(Protocol):
    async def scan(self, object_ref: str) -> ScanResult:
        ...
```

Possible implementations:

```text
ClamAV/local scanner
managed scanning service
provider integration
```

Do not hard-wire a scanner vendor into business logic.

## Parser safety

A file can be valid for its MIME type and still be malicious or resource-exhausting when parsed.

For document/image/archive processing, define:

- parser timeout
- memory limits where possible
- decompression limits
- page/object limits
- recursion limits
- worker isolation for high-risk parsers

Never treat a successful upload as a successful parse.

## Storage abstraction

Use an interface:

```python
class ObjectStorage(Protocol):
    async def put(...): ...
    async def get(...): ...
    async def delete(...): ...
    async def exists(...): ...
    async def generate_download_url(...): ...
```

Implementations can include:

```text
LocalObjectStorage
S3ObjectStorage
other cloud/provider implementation
```

The application/service layer should depend on `ObjectStorage`, not a vendor SDK.

## Database metadata

Persist metadata such as:

```text
object_id
owner/tenant
storage_key
original_filename
media_type
size_bytes
checksum
scan_status
processing_status
created_at
expires_at
```

Use PostgreSQL as the metadata source of truth.

Do not store an OS path as the public file identifier.

## Download authorization

Never assume possessing an object ID grants access.

```text
request
  ↓
authentication
  ↓
authorization/tenant check
  ↓
load metadata
  ↓
issue response or signed URL
```

Return `404` instead of `403` where the security policy intentionally avoids resource enumeration. Make this an explicit policy decision.

## Signed URLs

Presigned URLs are bearer capabilities. AWS documents that possession of a presigned URL grants the ability to perform the signed operation until expiration, subject to the creator's permissions and credential lifetime. [Certain] 

Rules:

- short expiration
- narrow object key
- narrow HTTP method
- narrow permissions
- no sensitive query logging
- authorization before issuing the URL
- never treat the URL as proof of identity

For uploads, bind the URL to the intended object key and expected content properties where the provider supports it. AWS also documents checksum verification for presigned uploads. [Certain]

## Direct-to-object-storage upload

For large files:

```text
client
  ↓
POST /uploads
  ↓
authorize + create object record
  ↓
short-lived signed upload URL
  ↓
client → object storage
  ↓
completion/verification
  ↓
mark object accepted
```

Do not mark the object fully trusted merely because the upload URL was used.

## Download choices

### API-proxied download

Useful when authorization or transformation must happen in the API.

### Signed download URL

Useful for large objects and private object storage.

### Public object URL

Use only when the resource is intentionally public.

## Streaming downloads

For large local files, use `FileResponse` or an appropriate streaming response rather than reading the entire file into memory.

For object storage, use provider streaming APIs or signed URLs.

## Range requests

Support HTTP range semantics when large media/file clients need resumable downloads. Do not implement ad hoc `Range` handling if the chosen storage/response layer already provides it safely.

## Temporary files

Use a dedicated temporary/quarantine location:

```text
var/tmp
var/quarantine
```

Cleanup must account for:

- successful processing
- validation failure
- cancellation
- timeout
- worker crash recovery

Do not delete a temp file while a background worker still needs it.

## Deduplication/checksums

A content checksum can be useful for:

- integrity verification
- deduplication
- cache identity

A checksum is not a malware scanner and is not an authorization mechanism.

## Retention and deletion

Define lifecycle rules:

```text
created
active
expired
deleted
legal-hold (if required)
```

Deletion should remove both metadata and storage objects according to an explicit consistency policy.

## Multi-tenant isolation

Object keys should include a tenant/resource boundary where helpful:

```text
tenant/{tenant_id}/objects/{object_id}
```

But the key is not the authorization control. The API must still enforce ownership/tenant policy.

## Forbidden patterns

- trusting `Content-Type`
- trusting original filenames
- using user filenames as filesystem paths
- reading unbounded files into memory
- exposing quarantined files
- returning private objects without authorization
- public buckets for convenience
- long-lived signed URLs without a business reason
- storing durable files only on replica-local disks
- quota checks without concurrency control
- hard-wiring a storage/scanner vendor into services
- parsing untrusted documents inside the request process when the parser is high-risk/heavy
