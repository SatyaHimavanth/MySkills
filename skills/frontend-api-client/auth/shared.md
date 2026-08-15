# Auth Token Handling — Shared

## Verified working mutator + refresh interceptor
This exact code was run against a live backend: register → login → poison the access token → make a request → confirm the interceptor transparently refreshes and retries → confirm the retried request succeeds. All five steps passed.

```ts
// src/api/axios-instance.ts
import axios from 'axios';

export const axiosInstance = axios.create({ baseURL: 'http://127.0.0.1:8000' });

let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setTokens(access: string, refresh: string) {
  accessToken = access;
  refreshToken = refresh;
}

axiosInstance.interceptors.request.use((config) => {
  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && refreshToken && !original._retried) {
      original._retried = true;
      try {
        const { data } = await axios.post('http://127.0.0.1:8000/api/v1/auth/refresh', {
          refresh_token: refreshToken,
        });
        setTokens(data.access_token, data.refresh_token);
        original.headers.Authorization = `Bearer ${data.access_token}`;
        return axiosInstance(original);
      } catch (refreshError) {
        // Terminal failure — the refresh token is dead too (expired, or revoked via
        // token_version, e.g. an account-takeover response on the backend). Verified:
        // without this, the caller sees the refresh endpoint's own generic "Invalid
        // credentials" error attached to whatever request triggered it — confusing, wrong
        // context — and the dead tokens stay in memory, so every subsequent request repeats
        // the same doomed refresh attempt instead of failing fast.
        accessToken = null;
        refreshToken = null;
        window.dispatchEvent(new CustomEvent('session-terminated'));
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  },
);

// Orval's react-query mode calls custom mutators fetch-style: (url, RequestInit).
// See codegen/shared.md's Forbidden section for what breaks if this signature is wrong.
export const apiClient = <T>(url: string, options?: RequestInit): Promise<T> =>
  axiosInstance({
    url,
    method: (options?.method as any) ?? 'GET',
    headers: options?.headers as Record<string, string>,
    data: options?.body,
  }).then((response) => response.data);
```

## `_retried` flag
Without it, a persistently-invalid refresh token causes infinite retry recursion — one failed refresh must be terminal, not retried again.

## Token storage
In-memory module state (as above) survives only the page session — acceptable for an SPA that re-authenticates on reload via a stored refresh token in an `httpOnly` cookie (server-set, never accessible to JS — see `fastapi-production`'s `security/csrf.shared.md` for the cookie-vs-bearer tradeoffs this implies on the backend side). Never store the access or refresh token in `localStorage`/`sessionStorage` — both are readable by any script on the page, making them a direct XSS exfiltration target.

## Forbidden
- storing tokens in localStorage/sessionStorage
- a refresh retry loop with no terminal-failure flag
- attaching the access token to requests going to a different origin than the API (leaks the token to third parties)
- letting a terminal refresh failure surface as the refresh endpoint's own generic error message with no dead-token cleanup and no app-level signal — verified this leaves stale tokens in memory (every subsequent request repeats the same doomed refresh) and shows the user a confusing out-of-context error instead of prompting re-authentication
