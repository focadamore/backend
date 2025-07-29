from datetime import date

from fastapi import Body, APIRouter, Query

from src.api.dependencies import DBDep
from src.exceptions import InvalidDatesRangeException, RoomNotFoundHTTPException, \
    HotelNotFoundException, HotelNotFoundHTTPException, InvalidDatesRangeHTTPException, RoomNotFoundException
from src.schemas.rooms import RoomsAddRequest, RoomsPatchRequest, Rooms
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms", summary="Просмотр всех номеров отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-06-29"),
    date_to: date = Query(example="2025-07-10"),
):
    try:
        rooms_data = await RoomService(db).get_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    except InvalidDatesRangeException as ex:
        raise InvalidDatesRangeHTTPException
    return rooms_data


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера по id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        room_data = await RoomService(db).get_room(room_id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return room_data


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def add_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomsAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "С описанием",
                "value": {
                    "title": "Двухместный люкс",
                    "description": "2-места, кондиционер, балкон",
                    "price": "10000",
                    "quantity": "4",
                    "facilities_ids": [3, 4],
                },
            },
            "2": {
                "summary": "Без описания",
                "value": {
                    "title": "Одноместный обычный",
                    "description": "",
                    "price": "5000",
                    "quantity": "8",
                    "facilities_ids": [],
                },
            },
        }
    ),
):

    try:
        room: Rooms = await RoomService(db).add_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    data = RoomService(db).delete_room(room_id=room_id, hotel_id=hotel_id)
    return {"data": data}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение всех данных номера")
async def change_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomsAddRequest):
    try:
        await RoomService(db).change_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": 200}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменение одного или нескольких тэгов номера")
async def change_room_partially(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomsPatchRequest
):
    try:
        await RoomService(db).change_room_partially(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": 200}
