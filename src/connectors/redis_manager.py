import redis.asyncio as redis
from typing import Any


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client: redis.Redis | None = None

    async def connect(self) -> None:
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            decode_responses=True  # Автоматически декодировать ответы в строки
        )
        try:
            await self.client.ping()
            print("Успешное подключение к Redis")
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")
            raise

    async def set(self, key: str, value: Any, expire: int | None = None) -> bool:
        if self.client is None:
            raise ConnectionError("Сначала нужно подключиться к Redis")

        if expire is not None:
            return await self.client.setex(key, expire, value)
        else:
            return await self.client.set(key, value)

    async def get(self, key: str) -> Any | None:
        if self.client is None:
            raise ConnectionError("Сначала нужно подключиться к Redis")

        return await self.client.get(key)

    async def delete(self, *keys: str) -> int:
        if self.client is None:
            raise ConnectionError("Сначала нужно подключиться к Redis")

        return await self.client.delete(*keys)

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None
            print("Успешное отключение от Redis")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
