import os
from typing import List
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""
    PORT: int = 8080
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = ["*"]
    
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
