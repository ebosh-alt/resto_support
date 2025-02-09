from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

from data.settings.base import ConfigBase


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_")
    bot_token: str


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")
    host: str


class RedisConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="redis_")
    host: str
    port: int


class ApiConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="api_")
    host: str


class Config(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()
