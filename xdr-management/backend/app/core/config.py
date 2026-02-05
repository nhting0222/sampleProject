from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "xdr-secret-key-change-in-production-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175"
    ]

    # App Info
    APP_NAME: str = "XDR Management API"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
