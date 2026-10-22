"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from maf import APP_VERSION
from maf.model_client import OpenAIAuthMode


class AppSettings(BaseSettings):
    """Settings for the agent service."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_version: str = APP_VERSION
    log_level: str = "INFO"
    enable_instrumentation: bool = True
    openai_base_url: str = "http://localhost:11434/v1"
    openai_chat_model: str = "qwen3:8b"
    openai_auth_mode: OpenAIAuthMode = OpenAIAuthMode.API_KEY
    openai_api_key: str | None = None

    @property
    def model_is_enabled(self) -> bool:
        return bool(self.openai_base_url.strip() and self.openai_chat_model.strip())


@lru_cache
def get_settings() -> AppSettings:
    """Load settings once per process; tests construct their own instances."""
    return AppSettings()
