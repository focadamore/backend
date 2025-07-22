from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

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
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data: BookingsAdd):
        room = await self.session.get(RoomsOrm, booking_data.room_id)
        # Получаем список доступных комнат в отеле на указанные даты
        available_rooms_query = rooms_ids_for_booking(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            hotel_id=room.hotel_id
        )

        available_rooms_query = available_rooms_query.where(RoomsOrm.id == booking_data.room_id)

        result = await self.session.execute(available_rooms_query)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Комната недоступна для бронирования на указанные даты"
            )

        new_booking = BookingsOrm(
            user_id=booking_data.user_id,
            room_id=booking_data.room_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            price=booking_data.price
        )

        self.session.add(new_booking)
        await self.session.flush()
        await self.session.refresh(new_booking)
        return BookingsDataMapper.map_to_domain_entity(new_booking)
