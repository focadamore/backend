from sqlalchemy import select, func, insert

from src.models.hotels import HotelsOrm
from src.database import engine
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, title, location, limit, offset):
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower().strip()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower().strip()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, **parameters):
        add_hotel_stmt = insert(HotelsOrm).values(**parameters).returning(HotelsOrm)
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_hotel_stmt)
        return result.scalars().all()
