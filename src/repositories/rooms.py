from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.exceptions import InvalidDatesRangeException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomsDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomsWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        if date_to <= date_from:
            raise InvalidDatesRangeException
        rooms_for_get_filtered = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_for_get_filtered))
        )
        result = await self.session.execute(query)
        return [
            RoomsWithRels.model_validate(model, from_attributes=True)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)  # type: ignore
        )
        result = await self.session.execute(query)
        model = result.scalar_one()
        return RoomsDataMapper.map_to_domain_entity(model)
