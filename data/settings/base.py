from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="data/.env", env_file_encoding="utf-8", extra="ignore"
    )
