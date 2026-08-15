# Runtime Validation — Shared

## Why types aren't enough
TypeScript types are erased at build time — nothing checks a real HTTP response actually matches them at runtime. A backend bug, a proxy/CDN mangling a response body, or a stale deployed frontend talking to a newer backend can all produce a response that type-checks at compile time but doesn't match reality at runtime. Zod schemas generated alongside the client (`codegen/shared.md`) close that gap.

## Where to validate
At the API boundary only — inside the generated client or a thin wrapper around it, not scattered through component code. Verified pattern:
```ts
import { CreateTaskApiV1TasksPostResponse } from './client.zod';

const task = await createTaskApiV1TasksPost({ title, description });
const validated = CreateTaskApiV1TasksPostResponse.parse(task); // throws on mismatch
```

## Validate requests too, not just responses
Verified: `TaskCreateBody.parse({ title: '' })` throws client-side (`min_length=1` violated) before any network call — catching an invalid request before spending a round trip on a 422 the backend would have returned anyway. Useful for immediate form-level feedback; it's a UX optimization, not a substitute for the backend's own validation, which remains the actual authority.

## Forbidden
- trusting a response's TypeScript type without runtime validation at the trust boundary
- duplicating validation rules by hand instead of using the generated Zod schemas (see `codegen/shared.md`'s fidelity note — the constraints are already there)
- silently swallowing a Zod parse failure — treat it as a real error (`error-handling/shared.md`), not a caught-and-ignored edge case
