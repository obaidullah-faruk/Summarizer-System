from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Backend API"
    version: str = "1.0.0"
    API_V1_prefix: str = "/api/v1"

    summary_ml_model: str = "Falconsai/text_summarization"
    summary_ml_max_length: int = 1000
    summary_ml_min_length: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
