# CSRF — Production

## Rules

- Enforce HTTPS.
- Use Secure/HttpOnly/SameSite cookie attributes according to the session design.
- Use a CSRF token/header mechanism for cookie-authenticated state-changing requests when required.
- Validate Origin/Referer or Fetch Metadata as defense in depth.
- Never use GET for state changes.
- Document explicit cross-origin exceptions such as webhooks.

## Multiple origins

CORS allowlists and CSRF trusted-origin policies must agree with the browser architecture.

Do not broaden one automatically because the other changed.

## Verification matrix

Validate the deployed browser flow with:

- same-origin mutation allowed
- cross-origin mutation rejected
- valid CSRF token accepted
- missing/invalid token rejected
- invalid Origin rejected
- expected SameSite/Secure/HttpOnly cookie attributes
- explicit webhook exceptions documented and independently authenticated

Do not rely on a staging manual check alone; include automated security tests for the chosen CSRF policy.
