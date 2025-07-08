from pathlib import Path
from pydantic_settings import SettingsConfigDict
from src.config import settings

from src.connectors.redis_manager import RedisManager

# model_config = SettingsConfigDict(env_file=f"{Path(__file__).parent.parent / '.env'}")

redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT
)
