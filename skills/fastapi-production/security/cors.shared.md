# CORS — Shared

## Purpose

Define browser cross-origin policy explicitly and separately from authentication/CSRF.

## Rules

- Treat `Origin` as the browser origin tuple: scheme + host + port.
- Allow only the origins the browser application actually needs.
- Do not use `*` when credentialed browser requests are required.
- Configure allowed methods and headers deliberately.
- Understand preflight `OPTIONS` requests.
- CORS does not replace authentication or CSRF protection.

## Example

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],
)
```

## Forbidden

- copying `allow_origins=["*"]` into production without reviewing credential requirements
- assuming CORS protects non-browser clients
- treating CORS as CSRF protection
