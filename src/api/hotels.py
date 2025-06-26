from fastapi import Body, Query, APIRouter

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotels, HotelsPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Hello page")
def func_main():
    """return hello"""
    return {"title": "Hello page!"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(id: int):
    # global hotels
    # hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
def change_hotel(hotel_id: int, hotel_data: Hotels):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "OK"}
        return {"status": "404 - Not Found"}


@router.patch("/{hotel_id}", summary="Изменение одного или нескольких тэгов отеля")
def change_hotel_lightly(id: int, hotel_data: HotelsPATCH):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = hotel_data.title or hotel["title"]
            hotel["name"] = hotel_data.name or hotel["name"]
            return {"status": "OK"}
        return {"status": "404 - Not Found"}


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
async def add_hotel(hotel_data: Hotels = Body(openapi_examples={
    "1": {"summary": "Дубай", "value": {"title": "Отель ХайСтар 4 звезды", "location": "Дубай, ул Центр 78"}},
    "2": {"summary": "Ялта", "value": {"title": "Отель Magic 3 звезды", "location": "Ялта, ул Набережная 6"}}
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(
            title=hotel_data.title,
            location=hotel_data.location
        )
        await session.commit()
        return {"status": "OK", "data": hotel}
