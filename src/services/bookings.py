from src.exceptions import RoomNotFoundException, ObjectNotFoundException, NoFreeRoomsLeftException
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.schemas.rooms import Rooms
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        bookings = await self.db.bookings.get_all()
        return bookings

    async def get_user_bookings(self, user_id: int):
        bookings = await self.db.bookings.get_filtered(user_id=user_id)
        return bookings

    async def add_booking(self, user_id: int, bookings_data: BookingsAddRequest):
        try:
            room: Rooms = await self.db.rooms.get_one(id=bookings_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        room_price: int = room.price
        _booking_data = BookingsAdd(
            user_id=user_id,
            price=room_price,
            **bookings_data.model_dump(),
        )
        try:
            await self.db.bookings.add_booking(_booking_data)
        except NoFreeRoomsLeftException as ex:
            raise NoFreeRoomsLeftException from ex
        await self.db.commit()
