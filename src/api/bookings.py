from fastapi import Body, APIRouter
from sqlalchemy import column

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.schemas.rooms import RoomsAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Забронировать номер")
async def add_booking(user_id: UserIdDep, db: DBDep, bookings_data: BookingsAddRequest):
    actual_price = await db.rooms.get_one_or_none(id=bookings_data.room_id)
    _bookings_data = BookingsAdd(**bookings_data.model_dump(), price=actual_price.price, user_id=user_id)
    booking = await db.bookings.add(_bookings_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("", summary="Просмотр всех бронирований")
async def get_all_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me", summary="Просмотр моих бронирований")
async def get_user_bookings(user_id: int, db: DBDep):
    bookings = await db.bookings.get_all(user_id=user_id)
    return {"status": "OK", "data": bookings}
