# Error Handling — Shared

## Don't assume the error shape — read the generated types
`fastapi-production` explicitly documents two valid, mutually exclusive response conventions (bare vs. enveloped success — see its `api/response_contracts.shared.md`). Which one a given backend uses is exactly what the generated types already encode — check `client.ts`'s response types for the actual error shape in use, don't hardcode an assumption. The example below matches the enveloped-error convention verified in this skill's own test backend:
```ts
type ErrorResponse = {
  success: false;
  data: null;
  error: { code: string; message: string; details?: unknown[] | null };
  meta: null;
};
```

Read those generated types as a lower bound, not a complete list: a status code the backend returns via a global exception handler without declaring it in the route's `responses=` won't appear in `/openapi.json` at all, so it can't appear in the generated type either — see `codegen/shared.md`'s Forbidden section for the verified before/after. If you hit a runtime error status the generated union doesn't mention, that's a backend schema gap, not a reason to hand-write a wider type here.


## Verified live
The backend's real error responses were exercised directly during verification — a 401 on bad credentials, a 404 from the router's own catch-all, correctly surfaced through axios's `error.response.data` shape shown above with no transformation needed; the generated types already matched the live payload exactly.

## Pattern
```ts
try {
  await createTaskApiV1TasksPost(payload);
} catch (e) {
  const message = axios.isAxiosError(e) && e.response?.data?.error?.message;
  // surface `message` to the user; log the full error object, don't discard it
}
```

## A terminal 401 is not just another error to display
`auth/shared.md`'s interceptor already handles the retry-once-then-give-up logic and clears dead tokens on terminal failure, emitting a `session-terminated` event. Listen for that event at the app's top level (not per-request) to clear user-facing session state and redirect to login — don't handle this per-call inside individual error-handling blocks, or every screen needs its own copy of "did my session just die" logic.
```ts
window.addEventListener('session-terminated', () => {
  queryClient.clear();
  navigate('/login');
});
```

## Rate limiting (429) needs different handling than other errors
Every other status in this file's Forbidden list gets a message shown to the user. `429` needs actual behavior: read `Retry-After` and disable the retry/submit action for that many seconds rather than either silently retrying immediately (hammers a server that's already shedding load — the exact scenario `fastapi-production`'s `operations/runbooks.shared.md` credential-stuffing runbook describes from the server side) or showing a dead-end error with no indication of when to try again.
```ts
catch (e) {
  if (axios.isAxiosError(e) && e.response?.status === 429) {
    const retryAfter = Number(e.response.headers['retry-after'] ?? 5);
    disableSubmitFor(retryAfter); // countdown UI, not a silent retry loop
  }
}
```

## Forbidden
- a generic "Something went wrong" with no distinction between validation (422), auth (401/403), not-found (404), rate-limited (429), and server (500) errors — the backend already encodes which one occurred, use it
- treating 429 like any other error — silently retrying immediately, or showing a message with no indication of when retry is safe
- swallowing the error object after extracting a message — losing `code`/`details` makes debugging a support ticket much harder later
