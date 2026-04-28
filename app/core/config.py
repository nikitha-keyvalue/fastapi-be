from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Values below are defaults when unset. Define APP_NAME, APP_VERSION,
    # DATABASE_URL, and SECRET_KEY in `.env` (or the process environment).
    APP_NAME: str = "FastAPI Backend"
    APP_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./app.db"

    SECRET_KEY: str = Field(
        ...,
        min_length=32,
        description="JWT signing key; required — set SECRET_KEY in .env",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
