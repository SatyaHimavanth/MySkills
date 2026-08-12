# CORS — Local Development

## Rules

- Add only the frontend development origins actually used.
- Keep ports explicit because `http://localhost:3000` and `http://localhost:5173` are different origins.
- Credentialed development requests must use explicit origins, not `*`.

Example:

```env
APP_CORS__ALLOWED_ORIGINS=["http://localhost:5173"]
APP_CORS__ALLOW_CREDENTIALS=true
```
