from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True,)
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    app_name: str = "Backend API"
    version: str = "1.0.0"
    API_V1_prefix: str = "/api/v1"

    summary_ml_model: str = "Falconsai/text_summarization"
    summary_ml_max_length: int = 1000
    summary_ml_min_length: int = 30


@lru_cache()
def get_settings() -> Settings:
    return Settings()
