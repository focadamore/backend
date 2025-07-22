import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", "r", encoding="utf-8") as file:
        hotels_data = json.load(file)
    with open("tests/mock_rooms.json", "r", encoding="utf-8") as file:
        rooms_data = json.load(file)

    async with async_session_maker_null_pool() as session:
        async with session.begin():
            for record in hotels_data:
                session.add(HotelsOrm(**record))
            for record in rooms_data:
                session.add(RoomsOrm(**record))


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "ant@mail.ru",
            "password": "1234"
        }
    )


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(ac, register_user):
    response = await ac.post(
        "auth/login",
        json={
            "email": "ant@mail.ru",
            "password": "1234"
        }
    )
    assert "access_token" in ac.cookies
    assert ac.cookies["access_token"]
    yield ac
