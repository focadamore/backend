from fastapi import Body, Query, APIRouter

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.base import BaseRepository
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelsAdd, HotelsPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Поиск отеля по id")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.get("",
            summary="Просмотр всех отелей",
            description="Много много премного текста")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(None, description="название отеля"),
                     location: str | None = Query(None, description="локация отеля"),
                     ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("", summary="Добавление нового отеля")
async def add_hotel(hotel_data: HotelsAdd = Body(openapi_examples={
    "1": {"summary": "Дубай", "value": {"title": "Отель ХайСтар 4 звезды", "location": "Дубай, ул Центр 78"}},
    "2": {"summary": "Ялта", "value": {"title": "Отель Magic 3 звезды", "location": "Ялта, ул Набережная 6"}}
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
        return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": 200}


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
async def change_hotel(hotel_id: int, hotel_data: HotelsAdd):
    async with async_session_maker() as session:
        found_hotels = await BaseRepository(session).get_all(id=hotel_id)
        if not found_hotels:
            return {"status": 404}
        if len(found_hotels) > 1:
            return {"status": 422}
        else:
            await HotelsRepository(session).edit(
                id=hotel_id,
                data=hotel_data
            )
            await session.commit()
            return {"status": 200}


@router.patch("/{hotel_id}", summary="Изменение одного или нескольких тэгов отеля")
async def change_hotel_partially(hotel_id: int, hotel_data: HotelsPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(id=hotel_id, exclude_unset=True, data=hotel_data)
        await session.commit()
        return {"status": 200}
