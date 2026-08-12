# CSRF Protection — Shared

## Purpose

Protect browser-authenticated state-changing requests when authentication credentials are automatically attached by the browser, especially cookies.

OWASP explains that cookies are automatically sent by browsers and recommends a real CSRF defense for state-changing operations; current guidance includes synchronizer tokens, double-submit patterns, custom headers, Fetch Metadata, and Origin verification depending on the architecture.

## First decision: bearer vs cookie authentication

### Bearer token in Authorization header

A typical API using:

```http
Authorization: Bearer <token>
```

is not automatically CSRF-vulnerable in the same way as cookie authentication because the browser does not automatically attach an arbitrary Authorization header cross-site.

Still evaluate other browser threats and XSS.

### Cookie/session authentication

The browser automatically includes cookies, so explicit CSRF protection is required for state-changing actions unless a very narrowly justified architecture satisfies all relevant conditions.

## Safe methods

Never perform state-changing operations through:

```text
GET
HEAD
OPTIONS
```

Use:

```text
POST
PUT
PATCH
DELETE
```

for state changes.

OWASP explicitly states that safe HTTP methods should not perform state-changing actions.

## Preferred SPA pattern

For browser SPAs using cookie authentication:

```text
server issues CSRF token
        ↓
client reads token
        ↓
state-changing request
        ↓
custom CSRF header
        ↓
server validates token/origin
```

Use a maintained implementation where available rather than inventing custom cryptographic token handling.

## Origin verification

For state-changing browser requests, compare the expected target origin with the `Origin` header when present.

If the application is behind a proxy, configure its public origin explicitly rather than deriving a trusted origin from an untrusted forwarded header.

OWASP recommends Origin/Referer verification as a defense-in-depth control.

## Fetch Metadata

For modern browser deployments, `Sec-Fetch-Site` can provide additional context.

A common policy:

```text
cross-site + state-changing method → reject
same-origin → allow
same-site → evaluate according to trust model
missing header → defined compatibility fallback
```

Do not treat Fetch Metadata as the only defense without considering clients that do not send it.

OWASP recommends a fallback such as standard origin verification or CSRF tokens and recommends a fail-safe policy for sensitive endpoints.

## SameSite cookies

Use an intentional SameSite policy:

```text
Strict
Lax
None
```

`SameSite` is defense in depth, not a universal replacement for CSRF tokens or origin verification.

For `SameSite=None`, the cookie must also be Secure.

## Cookie prefixes

For host-only cookies, prefer the `__Host-` prefix where applicable:

```text
__Host-session
```

It must use Secure, Path=/, and no Domain attribute.

## Webhooks

Do not apply browser CSRF mechanisms to server-to-server webhooks blindly.

Webhooks should use:

- signature verification
- timestamp/replay protection
- explicit source policy
- idempotency where necessary

## Login CSRF

Authentication endpoints can also be targeted by login-CSRF style attacks.

For browser cookie flows, include the same origin/CSRF protections where appropriate.

## Testing

Test:

- same-origin mutation allowed
- cross-origin mutation rejected
- missing/invalid CSRF token rejected
- invalid Origin rejected
- trusted same-site behavior according to policy
- missing Fetch Metadata header fallback
- safe-method state mutation rejected
- webhook flow remains functional without browser CSRF dependence

## Forbidden patterns

- relying only on CORS for CSRF prevention
- state changes through GET
- relying only on SameSite for all cookie-authenticated APIs
- inventing a custom token algorithm
- trusting Origin derived from an untrusted proxy header
- applying browser CSRF assumptions to server-to-server webhooks

## Sources

- https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

