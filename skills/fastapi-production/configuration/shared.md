# Configuration — Shared

## Purpose

Centralize application configuration into a single typed boundary using `pydantic-settings` to prevent scattered environment reads (`os.getenv()`) and enforce startup-time validation.

## Rules

- Use `pydantic-settings` (`BaseSettings` and `SettingsConfigDict`) as the sole configuration entry point.
- Load `.env` once at application startup, validate types, and inject settings via FastAPI dependency injection or `@lru_cache`.
- Use `SecretStr` for credentials and tokens to prevent accidental leak in logs or string dumps (`settings.db_password.get_secret_value()`).
- Group related configuration using nested Pydantic models with `env_nested_delimiter="__"`.
- Never scatter `os.getenv()` across application logic or route handlers.
- Required production settings (e.g. database URL, secret keys) must fail at startup if missing, rather than falling back to weak defaults.

## Recommended Pattern

```python
from functools import lru_cache
from pydantic import BaseModel, SecretStr, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseModel):
    url: PostgresDsn
    pool_size: int = 20
    max_overflow: int = 10

class AuthSettings(BaseModel):
    jwt_secret: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15

class Settings(BaseSettings):
    app_name: str = "FastAPI Backend"
    environment: str = "local"
    debug: bool = False
    
    db: DatabaseSettings
    auth: AuthSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Environment variable layout example:
```env
APP_NAME="Production API"
ENVIRONMENT="production"
DB__URL="postgresql+asyncpg://user:pass@db.example.com:5432/appdb"
AUTH__JWT_SECRET="super-secret-key-change-in-prod"
```

## Dependency Injection in Routes

```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/info")
async def get_info(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name, "environment": settings.environment}
```

## Forbidden Patterns

- Calling `os.getenv()` or `os.environ` directly in business services or route handlers
- Silent fallbacks to weak/insecure development keys when `ENVIRONMENT=production`
- Storing production secrets in source code or `.env` files checked into git
