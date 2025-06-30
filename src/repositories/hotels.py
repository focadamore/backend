from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_to_get
from src.schemas.hotels import Hotels


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotels

    async def get_filtered_by_time(self, title, location, limit, offset, date_from: date, date_to: date):
        rooms_for_get_filtered = rooms_ids_to_get(date_from=date_from, date_to=date_to)

        hotels_for_get_filtered = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_for_get_filtered))
        )

        if title:
            hotels_for_get_filtered = (hotels_for_get_filtered
                                       .filter(func.lower(HotelsOrm.title).contains(title.lower().strip())))
        if location:
            hotels_for_get_filtered = (hotels_for_get_filtered
                                       .filter(func.lower(HotelsOrm.location).contains(location.lower().strip())))
        hotels_for_get_filtered = (hotels_for_get_filtered
                                   .limit(limit)
                                   .offset(offset))

        return await self.get_filtered(HotelsOrm.id.in_(hotels_for_get_filtered))
