"""
Configuration management for the application.
Uses pydantic-settings for environment variable loading.
"""
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    app_name: str = "Zev Simple RAG AI Agent"
    app_version: str = "0.1.0"
    debug: bool = True

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # CORS
    backend_cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database (PostgreSQL)
    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str = "postgres"
    database_password: str = "6666"
    database_name: str = "postgres"

    # Gemini API
    gemini_api_key: str
    gemini_model: str = "gemini-3.1-pro-preview"

    # Chroma DB
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "zev_simple_rag_1_docs"

    # Knowledge base
    knowledge_base_path: str = "./knowledge_base"

    # Token counting (optional - for LangSmith)
    langsmith_api_key: Optional[str] = None
    langsmith_tracing: bool = False

    @property
    def database_url(self) -> str:
        """Construct the database URL from components."""
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
