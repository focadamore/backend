from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Список всех удобств")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Создание нового удобства")
async def add_facility(db: DBDep, data: FacilitiesAdd):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": 200, "data": facility}
