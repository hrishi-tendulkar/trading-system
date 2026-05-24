from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = Field(default="development", alias="ENVIRONMENT")
    app_base_url: str = Field(default="http://localhost:8000", alias="APP_BASE_URL")
    app_session_secret: str = Field(default="dummy-session-secret", alias="APP_SESSION_SECRET")
    app_shared_password_hash: str = Field(
        default="$2b$12$8KbQiF8zCqWgfQ6sPhQhKuDmjfZc1gA4V0y6ZzWnpr6MLd7q8fWNq",
        alias="APP_SHARED_PASSWORD_HASH",
    )
    csrf_secret: str = Field(default="dummy-csrf-secret", alias="CSRF_SECRET")
    supabase_url: str = Field(default="https://example.supabase.co", alias="SUPABASE_URL")
    supabase_service_role_key: str = Field(
        default="dummy-supabase-service-role-key",
        alias="SUPABASE_SERVICE_ROLE_KEY",
    )
    supabase_db_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/postgres",
        alias="SUPABASE_DB_URL",
    )
    fmp_api_key: str = Field(default="dummy-fmp-api-key", alias="FMP_API_KEY")
    openai_api_key: str = Field(default="dummy-openai-api-key", alias="OPENAI_API_KEY")
    sec_user_agent: str = Field(default="Trading System owner@example.com", alias="SEC_USER_AGENT")
    daily_run_enabled: bool = Field(default=True, alias="DAILY_RUN_ENABLED")
    weekly_run_enabled: bool = Field(default=True, alias="WEEKLY_RUN_ENABLED")
    ai_summary_max_symbols: int = Field(default=10, alias="AI_SUMMARY_MAX_SYMBOLS")
    login_rate_limit_attempts: int = Field(default=10, alias="LOGIN_RATE_LIMIT_ATTEMPTS")
    login_rate_limit_window_seconds: int = Field(default=900, alias="LOGIN_RATE_LIMIT_WINDOW_SECONDS")
    session_ttl_seconds: int = Field(default=604800, alias="SESSION_TTL_SECONDS")
    session_cookie_name: str = "trading_system_session"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
