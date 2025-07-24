from datetime import date

from fastapi import Body, Query, APIRouter, HTTPException

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import InvalidDatesRangeException, ObjectNotFoundException
from src.schemas.hotels import HotelsAdd, HotelsPatch, Hotels

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Поиск отеля по id")
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        hotel_data = await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель с указанными параметрами не найден")
    return hotel_data


@router.get("", summary="Просмотр всех отелей", description="Много много премного текста")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="название отеля"),
        location: str | None = Query(None, description="локация отеля"),
        date_from: date = Query(examples=["2025-06-29"]),
        date_to: date = Query(examples=["2025-07-10"]),
):
    per_page = pagination.per_page or 5
    try:
        hotel_data = await db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )
    except InvalidDatesRangeException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    return hotel_data


@router.post("", summary="Добавление нового отеля")
async def add_hotel(
        db: DBDep,
        hotel_data: HotelsAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Дубай",
                    "value": {"title": "Отель ХайСтар 4 звезды", "location": "Дубай, ул Центр 78"},
                },
                "2": {
                    "summary": "Ялта",
                    "value": {"title": "Отель Magic 3 звезды", "location": "Ялта, ул Набережная 6"},
                },
            }
        ),
):
    hotel: Hotels = await db.hotels.add(hotel_data)
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
async def change_hotel(db: DBDep, hotel_id: int, hotel_data: HotelsAdd):
    await db.hotels.edit(id=hotel_id, data=hotel_data)
    return {"status": 200}


@router.patch("/{hotel_id}", summary="Изменение одного или нескольких тэгов отеля")
async def change_hotel_partially(db: DBDep, hotel_id: int, hotel_data: HotelsPatch):
    await db.hotels.edit(id=hotel_id, exclude_unset=True, data=hotel_data)
    return {"status": 200}
