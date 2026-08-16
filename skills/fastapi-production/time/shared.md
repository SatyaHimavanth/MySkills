# Time and Date Handling — Shared

## Purpose

Prevent timezone, DST, expiration, multi-region clock drift, and timestamp inconsistency bugs across application services and database storage.

## Rules

- Use timezone-aware UTC datetimes for all instant timestamps (`datetime.now(timezone.utc)`).
- Do not use naive `datetime.utcnow()` for persisted application timestamps; prefer timezone-aware UTC values such as `datetime.now(timezone.utc)`. A bare `datetime.now()` is not itself deprecated, but it returns a naive local-time value and is unsafe for persisted instants unless the application explicitly requires that representation.
- Use `zoneinfo.ZoneInfo` for IANA timezone logic (e.g. `America/New_York`).
- Rely on the Database Primary Server Time (`server_default=func.now()`) for entity audit columns (`created_at`, `updated_at`) to eliminate application server clock skew across regions.
- When validating time-bounded security tokens (JWT `exp`, `nbf`, `iat`) in distributed multi-region systems, specify a clock skew leeway (e.g. `jwt.decode(..., leeway=10)`).
- Distinguish absolute instants (UTC), local calendar dates, wall-clock times, durations, and recurring local schedules.

## PostgreSQL / SQLAlchemy Time Pattern

```python
from datetime import datetime, timezone
import jwt
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[str] = mapped_column(primary_key=True)
    # Primary DB authoritative timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

def verify_distributed_token(token: str, secret_key: str) -> dict:
    # leeway=10 allows for up to 10 seconds of clock drift between auth server and app server
    return jwt.decode(token, secret_key, algorithms=["HS256"], leeway=10)
```

## Testing

Inject a testable clock dependency or freeze the application clock in tests rather than calling `time.sleep()`.
