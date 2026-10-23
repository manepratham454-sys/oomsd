import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    PROJECT_NAME: str = "EV Charging Station Management System"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./evcsms.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "evcsms_super_secret_jwt_key_2026_modern_oosmd_enterprise_grade")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:4173"
    ]
    SCHEDULER_INTERVAL_SECONDS: int = 60
    BOOKING_EXPIRATION_MINUTES: int = 10
    REMINDER_MINUTES_BEFORE: int = 15

settings = Settings()
