from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        extra="ignore",
    )

    secret_key: str
    database_url: PostgresDsn
    debug: bool = False
    allowed_hosts: str = ""
    secure_ssl_redirect: bool = True
    log_level: str = "INFO"


env = Env()
