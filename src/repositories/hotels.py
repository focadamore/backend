from sqlalchemy import select, func
from src.models.hotels import HotelsOrm
from src.database import engine
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotels


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotels

    async def get_all(self, title, location, limit, offset) -> list[Hotels]:
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
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
