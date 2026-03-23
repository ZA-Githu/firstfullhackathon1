from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    cohere_api_key: str = ""
    qdrant_url: str = ":memory:"
    qdrant_api_key: str = ""
    qdrant_collection: str = "ai-native-book"
    database_url: str = ""
    ingest_api_key: str = "my-ingest-secret-key"
    cors_origins: str = "http://localhost:3000,https://ismatz-hackathon1deploy.hf.space,https://your-github-username.github.io"
    environment: str = "development"
    github_token: str = ""
    max_answer_tokens: int = 150
    log_retention_days: int = 7
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
