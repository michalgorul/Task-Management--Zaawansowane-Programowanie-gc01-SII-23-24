import logging
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

USE_CACHED_SETTINGS = os.getenv("USE_CACHED_SETTINGS", "TRUE").lower == "true"  # type: ignore

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_database: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_cached_settings() -> Settings:
    """
    bypass pydantic's class instantiation by caching the method
    """
    return Settings()  # type: ignore


def get_settings() -> Settings:
    """
    will returned cached settings by default.
    :return: Settings instance
    """
    if USE_CACHED_SETTINGS:
        return get_cached_settings()
    else:
        return Settings()  # type: ignore
