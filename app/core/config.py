from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    APP_NAME: str = "Gesture AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Database configuration
    # For local development we default to SQLite. In production this would be overridden via env vars to PostgreSQL
    DATABASE_URL: str = "sqlite:///./database.db"

    # Cloudinary configuration
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    CLOUDINARY_URL: Optional[str] = None # Optional, Cloudinary SDK can use this directly
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
