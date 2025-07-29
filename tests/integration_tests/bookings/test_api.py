import pytest
from httpx import AsyncClient
from sqlalchemy import delete

from src.database import async_session_maker_null_pool
from src.models import BookingsOrm
from src.utils.db_manager import DBManager


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-02", "2024-08-11", 200),
        (1, "2024-08-03", "2024-08-12", 200),
        (1, "2024-08-04", "2024-08-13", 200),
        (1, "2024-08-05", "2024-08-14", 200),
        (1, "2024-08-06", "2024-08-15", 400),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db: DBManager, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="session")
async def delete_all_bookings(ac):
    async with async_session_maker_null_pool() as session:
        async with session.begin():
            await session.execute(delete(BookingsOrm))
    response = await ac.get("/bookings")
    assert response.status_code == 200


# @pytest.fixture(scope="module")
# async def delete_all_bookings():
#     async for _db in get_db_null_pool():
#         await _db.bookings.delete()
#         await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-02", "2024-08-11", 2),
        (1, "2024-08-03", "2024-08-12", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    delete_all_bookings,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    response_me = await authenticated_ac.get("/bookings/me")
    assert response_me.status_code == 200
    assert len(response_me.json()) == booked_rooms
