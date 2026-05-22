from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # ── API Keys ────────────────────────────────────────────────────────────
    GOOGLE_API_KEY: str
    OPENWEATHER_API_KEY: str
    NEWS_API_KEY: str
    SERP_API_KEY: str

    # ── App Config ──────────────────────────────────────────────────────────
    APP_ENV: str = "development"
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
