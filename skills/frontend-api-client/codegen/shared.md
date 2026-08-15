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
- **The custom mutator must match the fetch-style signature Orval's `react-query` mode actually calls it with — `(url: string, options?: RequestInit) => Promise<T>` — not a single `AxiosRequestConfig` object.** Verified: writing the mutator with an axios-style single-argument signature silently received the URL string as the "config" object; `axios(urlString)` defaults to GET, so every POST/PATCH/DELETE silently became a GET and returned `405 Method Not Allowed` with no error anywhere in the codegen step — it only surfaced at request time. See `auth/shared.md` for the correct mutator implementation.
- Never hand-edit generated output — see `SKILL.md`.
