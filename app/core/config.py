from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENVIRONMENT: Literal["local", "staging", "production"] = Field(default="local")
    PROJECT_NAME: str = Field(default="Replay Scraper API")
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )

    ANTICAPTCHA_API_KEY: str = Field(...)
    SITE_KEY: str = Field(...)

    AWS_REGION: str = Field(default="us-east-1")
    AWS_ACCESS_KEY_ID: str = Field(...)
    AWS_SECRET_ACCESS_KEY: str = Field(...)
    S3_BUCKET_NAME: str = Field(...)
    S3_REPLAYS_PREFIX: str = Field(default="replays/")


settings = Settings()
