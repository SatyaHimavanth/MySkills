# File Downloads — Shared

## Purpose

Define safe, authorized, efficient download behavior for local files and object storage.



## Response selection



Use the simplest safe response mechanism:



```text

small generated response → normal Response

local file → FileResponse

large generated stream → StreamingResponse

object storage → signed URL when practical

```



Do not load large files entirely into RAM just to return them.



## Authorization



Perform authorization before fetching or exposing a private object.



## Headers



Set appropriate:



- `Content-Type`

- `Content-Disposition`

- caching headers when explicitly safe

- `ETag`/conditional headers when the contract supports them



Do not place untrusted filenames directly into `Content-Disposition` without safe encoding.



## Range requests



Use a framework/storage implementation that correctly supports range requests rather than inventing custom byte-range logic casually.



## Error semantics



Missing private object may intentionally return `404` to avoid exposing existence. This must be a deliberate security policy.
