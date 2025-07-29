from src.schemas.facilities import Facilities, FacilitiesAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_facilities(self):
        print("из БД")
        return await self.db.facilities.get_all()

    async def add_facility(self, data: FacilitiesAdd):
        facility: Facilities = await self.db.facilities.add(data)
        await self.db.commit()

        return facility
