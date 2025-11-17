from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "DeepGuard Well Integrity API"
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/deepguard"
    cors_origins: str = "*"
    jwt_secret: str = "super-secret-change-me"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
