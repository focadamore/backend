from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.exceptions import NoFreeRoomsLeftException
from src.models import RoomsOrm
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingsAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def get_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data: BookingsAdd):
        room = await self.session.get(RoomsOrm, booking_data.room_id)
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            hotel_id=room.hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if booking_data.room_id in rooms_ids_to_book:
            new_booking = await self.add(booking_data)
            return new_booking

        raise NoFreeRoomsLeftException
