from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, NoFreeRoomsLeftException
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.schemas.rooms import Rooms

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Просмотр всех бронирований")
async def get_all_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me", summary="Просмотр моих бронирований")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Забронировать номер")
async def add_booking(user_id: UserIdDep, db: DBDep, bookings_data: BookingsAddRequest):
    try:
        room: Rooms = await db.rooms.get_one(id=bookings_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    room_price: int = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **bookings_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data)
    except NoFreeRoomsLeftException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
