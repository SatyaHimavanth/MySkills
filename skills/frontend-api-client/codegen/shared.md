# Client & Schema Generation — Shared

## Purpose
Generate a typed client and runtime validators directly from the backend's OpenAPI schema. Verified via Orval 8.x against a live FastAPI backend — this file documents what actually worked, including two real bugs hit along the way.

## Setup
```ts
// orval.config.ts
import { defineConfig } from 'orval';

export default defineConfig({
  api: {
    input: 'http://127.0.0.1:8000/openapi.json',
    output: {
      target: './src/api/client.ts',
      client: 'react-query',
      override: { mutator: { path: './src/api/axios-instance.ts', name: 'apiClient' } },
    },
  },
  apiZod: {
    input: 'http://127.0.0.1:8000/openapi.json',
    output: { target: './src/api/client.zod.ts', client: 'zod' },
  },
});
```
Run: `npx orval`. Requires the backend running and reachable at `input` — codegen reads the live schema, not a checked-in copy of it.

## Verified fidelity
Orval carries real Pydantic constraints through to both TypeScript types and Zod schemas, not just field names/types — confirmed directly: `Field(min_length=8, max_length=128)` on a backend password field produced `passwordMin = 8` / `passwordMax = 128` constants and a matching Zod `.min(8).max(128)`, with zero manual frontend-side re-declaration of that rule.

## Forbidden — two real bugs found running this

- **Do not set `output.baseUrl`** if the backend's OpenAPI paths already include a prefix (e.g. FastAPI routes registered under `/api/v1/...`). Verified: adding `baseUrl: '/api'` on top of paths that already start with `/api/v1/...` produced `/api/api/v1/...` and every request 404'd. The base host belongs on the axios instance (`auth/shared.md`), not here.
- **Do not assume the React Query client choice determines one universal custom-mutator signature.** Match the mutator contract to the HTTP client configured for Orval. For the fetch-style client used by this skill, use `(url: string, options?: RequestInit) => Promise<T>`; an Axios-based mutator needs the Axios contract expected by the configured client. Verify the generated call shape after changing `client`/`httpClient` configuration. See `auth/shared.md` for this skill's fetch-style example.
- Never hand-edit generated output — see `SKILL.md`.
- **Don't trust a clean `npx orval` run to mean the error types are complete.** Verified against a live backend: a route that correctly returns `409`/`401`/`429` at runtime via a FastAPI `@app.exception_handler` produced a generated mutation-error type of `HTTPValidationError` only — codegen ran without any error or warning, and the type was simply wrong-by-omission. The cause is on the backend: those status codes weren't in `/openapi.json` because a global exception handler doesn't register itself in the schema (see `fastapi-production`'s `api/response_contracts.shared.md` for the fix — routes must declare non-2xx codes via `responses=`). After that fix, regenerating produced `ErrorResponseSchema | HTTPValidationError`, confirmed by re-running `npx orval` and diffing the output. If a status code you know the backend returns is missing from a generated mutation-error type, treat it as a backend schema gap, not a codegen bug — check `/openapi.json` directly before debugging the frontend.

