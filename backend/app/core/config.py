import os
from typing import List, Optional
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""
    PORT: int = 8080
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    JWT_SECRET_KEY: str = "your_super_secret_jwt_key_here"
    RATE_LIMIT_PER_MINUTE: int = 10
    UPLOAD_RATE_LIMIT: int = 3
    DATABASE_URL: str = "postgresql://klyvix_user:supersecretpassword@localhost:5432/klyvix"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379"
    
    # Model defaults
    GEMINI_MODEL: str = "gemini-2.0-flash-lite"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    MISTRAL_MODEL: str = "codestral-latest"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
