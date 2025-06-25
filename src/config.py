from pydantic_settings import SettingsConfigDict, BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=f"{Path(__file__).parent.parent / '.env'}")


settings = Settings()
