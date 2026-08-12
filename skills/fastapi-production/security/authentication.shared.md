# Authentication — Shared

## Purpose

Define a secure, testable authentication boundary for FastAPI applications using `OAuth2PasswordBearer`, `PyJWT`, centralized dependency injection, and strict active-user verification for token refresh cycles.

## Rules

- Authentication must be explicit, consistent, and scope-aware.
- Use FastAPI security dependencies (`OAuth2PasswordBearer`, `Security`) for auth boundaries.
- Use `PyJWT` for token encoding/decoding (`python-jose` is unmaintained).
- Centralize token verification and identity loading in a dependency (`get_current_user`).
- **Active User Database Check on Token Refresh**: Refresh token handlers **must query PostgreSQL** to confirm that:
  1. The user exists in the database.
  2. The account is active (`user.is_active is True` — not disabled, suspended, or soft-deleted).
  3. The refresh token has not been revoked or invalidated in database/Redis storage.
- Distinguish unauthenticated (`401 Unauthorized` with `WWW-Authenticate: Bearer` header) from unauthorized (`403 Forbidden`).
- Never put token validation or secret key handling directly inside route handlers.

## Architecture & Active-User Check Snippet

```python
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, SecretStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class TokenData(BaseModel):
    user_id: str
    scopes: list[str] = []

def create_token(data: dict, secret_key: SecretStr, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key.get_secret_value(), algorithm="HS256")

async def refresh_tokens(
    refresh_token: str,
    db: AsyncSession,
    jwt_secret: SecretStr,
) -> dict:
    """Exchange a valid refresh token for a new access token after verifying user status in DB."""
    try:
        payload = jwt.decode(refresh_token, jwt_secret.get_secret_value(), algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id: str = payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # CRITICAL SECURITY CHECK: Fetch user from DB to verify account state
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive, disabled, or non-existent",
        )

    # Produce new token pair after DB validation passes
    new_access_token = create_token({"sub": user.id, "type": "access"}, jwt_secret, timedelta(minutes=15))
    return {"access_token": new_access_token, "token_type": "bearer"}
```

## Threat-Model Note

Authentication mechanisms should be selected from the application's client and identity model. Browser sessions, machine-to-machine service accounts, enterprise OIDC, and public bearer-token APIs have different security requirements.

Do not introduce OAuth2 password login merely because FastAPI documents an example; use it only when the application actually owns user credentials and the OAuth2 password grant is appropriate for the architecture.

## Forbidden

- issuing refresh or access tokens without verifying `user.is_active` against the database
- hardcoded JWT secret keys or algorithm defaults
- omitting `algorithms=["HS256"]` in `jwt.decode` (prevents algorithm confusion attacks like `"none"`)
- returning generic 500 errors on invalid/expired tokens
- storing session state in JWT payloads without expiration
