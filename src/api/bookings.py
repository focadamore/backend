from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Просмотр всех бронирований")
async def get_all_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me", summary="Просмотр моих бронирований")
async def get_user_bookings(user_id: int, db: DBDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}


@router.post("", summary="Забронировать номер")
async def add_booking(user_id: UserIdDep, db: DBDep, bookings_data: BookingsAddRequest):
    room = await db.rooms.get_one_or_none(id=bookings_data.room_id)
    room_price: int = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **bookings_data.model_dump(),
    )
    booking = await db.bookings.add_booking(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
