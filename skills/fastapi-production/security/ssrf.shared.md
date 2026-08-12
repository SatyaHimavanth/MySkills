# SSRF Protection — Shared

## Purpose

Prevent server-side request forgery when the application fetches a URL, connects to a host supplied by a user, follows a webhook target, imports a remote document, or otherwise turns user-controlled network input into an outbound request.

OWASP recommends different defenses depending on whether targets can be allowlisted, and warns that URL validation is difficult, redirects can bypass validation, and DNS resolution can create pinning/rebinding problems. [Certain] OWASP API7 is Server-Side Request Forgery. 

## First decision: can targets be allowlisted?

### Case A — known trusted targets

Prefer an explicit allowlist:

```text
user input
   ↓
normalize/parse
   ↓
allowed scheme
   ↓
allowed hostname
   ↓
allowed port
   ↓
network policy
   ↓
HTTP client
```

This is the preferred design when the application only needs a known set of external services.

### Case B — arbitrary public targets are a real requirement

If users must provide arbitrary public URLs, application-layer filtering is harder. Combine strict URL parsing with network egress controls, private-range protections, DNS-aware validation, short timeouts, disabled redirects, and outbound network policy.

OWASP explicitly recommends network-layer controls in addition to application validation for SSRF defense in depth.

## Accepted schemes

Prefer an allowlist such as:

```text
https
```

Allow `http` only when the business requirement explicitly requires it.

Reject schemes such as:

```text
file
ftp
gopher
smb
phar
data
dict
```

Do not assume the HTTP client will make unsupported schemes harmless.

## URL validation

Parse URLs with a battle-tested parser.

Validate:

- scheme
- hostname
- port
- credentials/userinfo
- path/query where relevant

Reject userinfo in security-sensitive outbound URLs unless explicitly required:

```text
https://user:password@example.com/
```

Do not use a regex as the primary URL parser.

## Host/IP checks

Block destinations that are not allowed by the business policy, including:

- loopback
- private RFC1918 networks
- link-local addresses
- unspecified addresses
- multicast addresses
- cloud metadata endpoints
- internal corporate ranges unless explicitly allowlisted

Check both IPv4 and IPv6.

Python's `ipaddress` module provides structured address properties such as `is_private`, `is_loopback`, `is_link_local`, and `is_global`; use a standard library parser rather than hand-written IP parsing.

## DNS rebinding

A domain can resolve to different addresses over time. A string allowlist such as `example.com` does not by itself prove the actual connection will reach a safe public endpoint.

For high-risk arbitrary-target fetching:

1. resolve the hostname with a controlled resolver strategy
2. inspect all A/AAAA results
3. reject disallowed addresses
4. ensure the actual connection cannot bypass the validated destination
5. consider network egress restrictions as the final control

Do not assume a single DNS lookup completely eliminates rebinding risk. OWASP calls out DNS pinning/rebinding as a specific SSRF concern.

## Redirects

Disable automatic redirect following for SSRF-sensitive fetchers unless redirects are explicitly required and revalidated at every hop.

If redirects are allowed:

```text
request target
   ↓
response 30x
   ↓
parse Location
   ↓
repeat SSRF validation
   ↓
follow only if destination remains allowed
```

Never validate only the initial URL and then blindly follow redirects.

## Ports

Prefer an explicit port allowlist where possible.

For example:

```text
443 only
```

is safer than accepting arbitrary ports for an HTTPS fetch feature.

## HTTP client configuration

Use the project's shared `httpx.AsyncClient` infrastructure and apply a dedicated SSRF-safe policy.

Set:

- strict connect timeout
- read timeout
- write timeout
- pool timeout
- maximum response size
- redirects disabled by default
- TLS verification enabled

## Response handling

Do not blindly proxy arbitrary upstream responses to clients.

Validate:

- status code
- content type
- response size
- expected schema/content

Store/download only the data the business flow requires.

## Metadata services

Cloud metadata endpoints are high-risk SSRF targets.

Network-level egress controls should block metadata access unless the deployment explicitly requires it.

Where the cloud platform supports a hardened metadata protocol, use it according to platform guidance.

## File/URL ingestion

Features such as:

```text
import image from URL
import document from URL
webhook tester
remote avatar
URL preview
```

must route through the SSRF protection boundary.

Do not let feature code call `httpx.get(user_url)` directly.

## Architecture

```python
class SafeFetcher(Protocol):
    async def fetch(self, target: RemoteTarget) -> FetchResult: ...
```

The service receives a validated `RemoteTarget`, not an arbitrary URL string.

## Testing

Test:

- allowed public host
- blocked localhost
- blocked private IPv4
- blocked private IPv6
- blocked link-local address
- blocked metadata address/domain
- disallowed scheme
- disallowed port
- redirects to blocked destinations
- DNS results containing mixed public/private addresses
- oversized response
- timeout

## Forbidden patterns

- `httpx.get(user_supplied_url)`
- trusting URL strings because they start with `https://`
- allowing redirects without revalidation
- validating hostname but ignoring resolved IPs
- validating only IPv4
- accepting arbitrary schemes
- using a generic external HTTP client for both safe internal calls and SSRF-sensitive arbitrary fetches

## Sources

- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html

