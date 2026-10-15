"""Centralized local configuration; never hard-code production secrets."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://gridpulse:gridpulse@localhost:5432/gridpulse"
    log_level: str = "INFO"
    timezone_storage: str = "UTC"
    timezone_reporting: str = "Europe/Paris"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
