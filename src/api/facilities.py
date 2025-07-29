from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd, Facilities
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Список всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("из БД")
    return await FacilityService(db).get_facilities()


@router.post("", summary="Создание нового удобства")
async def add_facility(db: DBDep, data: FacilitiesAdd):
    facility: Facilities = await FacilityService(db).add_facility(data)
    return {"status": 200, "data": facility}
