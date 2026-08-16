from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Software Engineering System"
    app_env: str = "development"
    database_url: str = "sqlite:///./url_shortener.db"
    log_level: str = "INFO"
    short_code_length: int = 7
    max_retries: int = 2
    approval_required: bool = True
    llm_provider: str = "deterministic"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
