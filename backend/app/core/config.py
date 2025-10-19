from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, )
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    JWT_SECRET: str
    JWT_ACCESS_TOKEN_VALIDITY: int
    JWT_REFRESH_TOKEN_VALIDITY: int
    JWT_ALGORITHM: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    REDIS_SERVER: str
    REDIS_PORT: str

    app_name: str = "Backend API"
    version: str = "1.0.0"
    API_V1_prefix: str = "/api/v1"

    summary_ml_model: str = "Falconsai/text_summarization"
    summary_ml_max_length: int = 1000
    summary_ml_min_length: int = 30


@lru_cache()
def get_settings() -> Settings:
    return Settings()
