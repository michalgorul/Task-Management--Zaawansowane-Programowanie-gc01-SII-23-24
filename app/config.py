import logging

from pydantic_settings import BaseSettings

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

    class Config:
        env_file = "ENV/local.env"
        env_file_encoding = "utf-8"


settings = Settings()
