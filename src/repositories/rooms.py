from sqlalchemy import select, func

from src.database import engine
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    # async def get_all(self, title, price, hotel_id) -> list[Rooms]:
    #     query = select(RoomsOrm).filter_by(hotel_id=hotel_id)
    #     if title:
    #         query = query.filter(func.lower(RoomsOrm.title).contains(title.lower().strip()))
    #     if price:
    #         query = query.filter(RoomsOrm.price == price)
    #     print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(query)
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
