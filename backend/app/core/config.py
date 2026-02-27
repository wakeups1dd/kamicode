"""
KamiCode — Core Configuration

Reads all configuration from environment variables using Pydantic Settings.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve project root (.env is at d:\kamicode\.env, this file is at d:\kamicode\backend\app\core\config.py)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # backend/../..


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=str(_PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ─── Application ───────────────────────────────────────────────
    ENVIRONMENT: str = "dev"
    DEBUG: bool = True
    APP_NAME: str = "KamiCode"
    APP_VERSION: str = "0.1.0"

    # ─── Database ──────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./kamicode.db"
    DATABASE_URL_SYNC: str = "sqlite:///./kamicode.db"
    USE_SQLITE: bool = True  # Set to False when PostgreSQL is available

    # ─── Redis ─────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ─── Auth / JWT ────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production-use-a-64-char-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ─── AI Engine ─────────────────────────────────────────────────
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    AI_MODEL: str = "gemini-2.5-flash"

    # ─── Blockchain ────────────────────────────────────────────────
    CHAIN_RPC_URL: str = "https://sepolia.base.org"
    MINTER_PRIVATE_KEY: Optional[str] = None
    CONTRACT_ADDRESS: str = "0x0000000000000000000000000000000000000000"

    # ─── IPFS (Pinata) ─────────────────────────────────────────────
    PINATA_API_KEY: Optional[str] = None
    PINATA_SECRET_KEY: Optional[str] = None

    # ─── CORS ──────────────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # ─── Celery ────────────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "prod"


@lru_cache()
def get_settings() -> Settings:
    """Cached singleton for application settings."""
    return Settings()
