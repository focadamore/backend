from fastapi import Body, APIRouter
from sqlalchemy import column

from src.api.dependencies import DBDep
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.schemas.rooms import RoomsAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Забронировать номер")
async def add_booking(db: DBDep, bookings_data: BookingsAddRequest = Body(openapi_examples={
    "1": {"summary": "тестовая бронь",
          "value": {"date_from": "2025-07-01",
                    "date_to": "2025-07-14",
                    "room_id": "3"
                    }}
})):
    actual_price = await db.rooms.get_one_or_none(id=bookings_data.room_id)
    _bookings_data = BookingsAdd(**bookings_data.model_dump(), price=actual_price.price, user_id=22)
    booking = await db.bookings.add(_bookings_data)
    return {"status": "OK", "data": booking}
