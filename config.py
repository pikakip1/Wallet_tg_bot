from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    TG_API_KEY: SecretStr

    DB_HOST: str
    DB_USER: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    env_file: ClassVar[Path] = Path(__file__).parent / '.env'
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8')

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Settings()
