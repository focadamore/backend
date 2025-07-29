from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import NoFreeRoomsLeftException, NoFreeRoomsLeftHTTPException, \
    RoomNotFoundHTTPException, RoomNotFoundException
from src.schemas.bookings import BookingsAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Просмотр всех бронирований")
async def get_all_bookings(db: DBDep):
    bookings = await BookingService(db).get_all_bookings()
    return {"status": "OK", "data": bookings}


@router.get("/me", summary="Просмотр моих бронирований")
async def get_user_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_user_bookings(user_id=user_id)


@router.post("", summary="Забронировать номер")
async def add_booking(user_id: UserIdDep, db: DBDep, bookings_data: BookingsAddRequest):
    try:
        booking = await BookingService(db).add_booking(user_id=user_id, bookings_data=bookings_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoFreeRoomsLeftException:
        raise NoFreeRoomsLeftHTTPException
    return {"status": "OK", "data": booking}
