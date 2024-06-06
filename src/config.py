import os
import secrets
from typing import Any, List, Optional, Type, Union, Tuple, Dict
from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource

env_path = os.path.join(os.getcwd(), ".env")


class Settings(BaseSettings):  # type: ignore
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return dotenv_settings, env_settings, init_settings, file_secret_settings

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_HOST: AnyHttpUrl
    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URI: Union[str, None] = None

    ENVIRONMENT: str = "dev"


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')  # type: ignore
