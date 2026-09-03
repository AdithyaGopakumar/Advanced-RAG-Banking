"""
Application configuration using pydantic-settings.

All settings are loaded from environment variables or .env file.
Access via: `from app.core.config import get_settings`
"""

from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── Application ───
    APP_NAME: str = "AI Recruitment Assistant"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ─── Server ───
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ─── Auth ───
    API_KEY: str = "dev-secret-key"

    # ─── CORS ───
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    ALLOWED_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    ALLOWED_HEADERS: list[str] = ["Authorization", "Content-Type", "X-API-Key", "X-Request-ID"]

    # ─── Trusted Hosts ───
    ALLOWED_HOSTS: list[str] = ["*"]  # Lock down in production (e.g., ["api.example.com"])

    # ─── Rate Limiting ───
    RATE_LIMIT: str = "100/minute"

    # ─── Logging ───
    LOG_LEVEL: str = "INFO"

    # ─── AI Agent Defaults ───
    DEFAULT_AGENT_TIMEOUT: float = 30.0
    DEFAULT_AGENT_RETRIES: int = 0

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Enforce safety checks when running in production."""
        if not self.is_production:
            return self

        errors: list[str] = []

        if self.DEBUG:
            errors.append("DEBUG must be False in production")

        if self.API_KEY == "dev-secret-key":
            errors.append("API_KEY must not be the default 'dev-secret-key' in production")

        if "*" in self.ALLOWED_HOSTS:
            errors.append(
                "ALLOWED_HOSTS must not contain '*' in production — "
                "set to your actual domain(s)"
            )

        if "*" in self.ALLOWED_ORIGINS:
            errors.append(
                "ALLOWED_ORIGINS must not contain '*' in production — "
                "set to your actual frontend origin(s)"
            )

        if errors:
            raise ValueError(
                "Invalid production configuration:\n  • " + "\n  • ".join(errors)
            )

        return self


@lru_cache()
def get_settings() -> Settings:
    """Cached singleton access to application settings."""
    return Settings()
