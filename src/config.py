# from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Конфигурационный класс"""
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    MODE: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
