from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_to_get
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_filtered_by_time(self,
                                   hotel_id: int,
                                   date_from: date,
                                   date_to: date):
        rooms_for_get_filtered = rooms_ids_to_get(date_from, date_to, hotel_id)

        return await self.get_filtered(RoomsOrm.id.in_(rooms_for_get_filtered))
