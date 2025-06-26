from fastapi import Body, Query, APIRouter
from sqlalchemy import insert, select, update, func
from sqlalchemy.sql.operators import like_op

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
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
        query = select(HotelsOrm)
        if title:
            query = query.where(func.lower(HotelsOrm.title).contains(func.lower(title)))
        if location:
            query = query.where(func.lower(HotelsOrm.location).contains(func.lower(location)))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    # return hotels_


@router.post("", summary="Добавление нового отеля")
async def add_hotel(hotel_data: Hotels = Body(openapi_examples={
    "1": {"summary": "Москва", "value": {"title": "Москва", "location": "Moscow"}},
    "2": {"summary": "Симферополь", "value": {"title": "Симф", "location": "Simf"}}
})):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
        return {"http_status": 200, "response": "OK"}
