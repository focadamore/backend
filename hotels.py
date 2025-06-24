from fastapi import Body, Query, APIRouter
from schemas.hotels import Hotels, HotelsPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Дубай", "name": "Dubai"},
    {"id": 2, "title": "Сочи", "name": "Sochi"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("/", summary="Hello page")
def func():
    """return hello"""
    return {"title": "Hello page!"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
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
def get_hotels(id: int | None = Query(None, description="id отеля"),
               title: str | None = Query(None, description="название отеля"),
               page: int | None = Query(1, description="номер страницы"),
               per_page: int | None = Query(2, description="количество записей на страницу")
               ):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if page == 1:
        start = page - 1
        return hotels_[start:per_page]
    else:
        start = page + per_page - 2
        limit = per_page * 2
        return hotels_[start:limit]


@router.post("", summary="Добавление нового отеля")
def add_hotel(hotel_data: Hotels = Body(openapi_examples={
    "1": {"summary": "Москва", "value": {"title": "Москва", "name": "Moscow"}},
    "2": {"summary": "Симферополь", "value": {"title": "Симф", "name": "Simf"}}
})):
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name
        }
    )
