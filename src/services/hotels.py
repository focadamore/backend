from datetime import date

from src.schemas.hotels import HotelsAdd, HotelsPatch
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date
    ):
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelsAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def change_hotel(self, hotel_id: int, hotel_data: HotelsAdd):
        await self.db.hotels.edit(id=hotel_id, data=hotel_data)
        await self.db.commit()

    async def change_hotel_partially(self, hotel_id: int, hotel_data: HotelsPatch):
        await self.db.hotels.edit(id=hotel_id, data=hotel_data, exclude_unset=True)
        await self.db.commit()
