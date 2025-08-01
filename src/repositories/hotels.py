from datetime import date

from sqlalchemy import select, func

from src.exceptions import InvalidDatesRangeException
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotels


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelsDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset,
    ) -> list[Hotels]:
        if date_to <= date_from:
            raise InvalidDatesRangeException
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
