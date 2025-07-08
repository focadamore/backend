from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Список всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("из БД")
    return await db.facilities.get_all()


@router.post("", summary="Создание нового удобства")
async def add_facility(db: DBDep, data: FacilitiesAdd):
    facility = await db.facilities.add(data)
    await db.commit()
    test_task.delay()

    return {"status": 200, "data": facility}
