"""SIG-UTCUTS Chile — Backend configuration."""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database — defaults to SQLite for local dev without Docker/PostGIS
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL",
        "sqlite:///./sigutcuts.db"
    )

    # JWT
    JWT_SECRET: str = "change_me_in_production_sigutcuts_2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440

    # CORS
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",")]

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

    # App
    APP_NAME: str = "SIG-UTCUTS Chile"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
