from fastapi import Body, APIRouter

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms", summary="Просмотр всех номеров отеля")
async def get_rooms(db: DBDep, hotel_id: int):
    return await db.rooms.get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск отеля по id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def add_room(db: DBDep, hotel_id: int, room_data: RoomsAddRequest = Body(openapi_examples={
    "1": {"summary": "С описанием",
          "value": {"title": "Двухместный люкс",
                    "description": "2-места, кондиционер, балкон",
                    "price": "10000",
                    "quantity": "4"}},
    "2": {"summary": "Без описания",
          "value": {"title": "Одноместный обычный",
                    "description": "",
                    "price": "5000",
                    "quantity": "8"}}
})):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    return {"status": 200}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение всех данных номера")
async def change_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomsAddRequest):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(id=room_id, data=_room_data)
    return {"status": 200}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменение одного или нескольких тэгов номера")
async def change_room_partially(db: DBDep, hotel_id: int, room_id: int, room_data: RoomsPatchRequest):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(id=room_id, hotel_id=hotel_id, exclude_unset=True, data=_room_data)
    return {"status": 200}
