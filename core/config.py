from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "fastapi"
    
    # MongoDB Connection Pool Settings
    MAX_POOL_SIZE: int = 10
    MIN_POOL_SIZE: int = 1
    MAX_IDLE_TIME_MS: int = 45000  # 45 seconds
    CONNECT_TIMEOUT_MS: int = 10000  # 10 seconds
    SOCKET_TIMEOUT_MS: Optional[int] = None  # No timeout
    SERVER_SELECTION_TIMEOUT_MS: int = 5000  # 5 seconds
    
    # Retry Settings
    MONGO_RETRY_ATTEMPTS: int = 3
    MONGO_RETRY_DELAY_MS: int = 1000  # 1 second

    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def CORS_ORIGINS(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
