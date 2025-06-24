from fastapi import Body, Query, APIRouter

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Дубай", "name": "Dubai"},
    {"id": 2, "title": "Сочи", "name": "Sochi"},
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
def change_hotel(id: int = Query(description="ID Отеля"),
                 title: str = Body(),
                 name: str = Body()
                 ):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
        return {"status": "404 - Not Found"}


@router.patch("/{hotel_id}", summary="Изменение одного или нескольких тэгов отеля")
def change_hotel_lightly(id: int,
                         title: str | None = Body(None),
                         name: str | None = Body(None)
                         ):
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title or hotel["title"]
            hotel["name"] = name or hotel["name"]
            return {"status": "OK"}
        return {"status": "404 - Not Found"}


@router.get("",
            summary="Просмотр всех отелей",
            description="Много много премного текста")
def get_hotels():
    return [hotel for hotel in hotels]


@router.post("", summary="Добавление нового отеля")
def add_hotel(title: str = Body(embed=True)):
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title
        }
    )
