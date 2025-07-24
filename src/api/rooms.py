from datetime import date

from fastapi import Body, APIRouter, Query, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import InvalidDatesRangeException, ObjectNotFoundException
from src.schemas.facilities import RoomsFacilitiesAdd
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, Rooms

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms", summary="Просмотр всех номеров отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-06-29"),
    date_to: date = Query(example="2025-07-10"),
):
    try:
        rooms_data = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    except InvalidDatesRangeException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    return rooms_data


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера по id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        room_data = await db.rooms.get_one(room_id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер с указанными параметрами не найден")
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
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room: Rooms = await db.rooms.add(_room_data)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    rooms_facilities_data = [
        RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    check_room_exists = db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    return {"data": check_room_exists}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение всех данных номера")
async def change_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomsAddRequest):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.edit(id=room_id, data=_room_data)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    await db.rooms_facilities.delete(room_id=room_id)
    rooms_facilities_data = [
        RoomsFacilitiesAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": 200}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменение одного или нескольких тэгов номера")
async def change_room_partially(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomsPatchRequest
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.edit(id=room_id, data=_room_data)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    current_facilities = await db.rooms_facilities.get_all(room_id=room_id)
    current_facility_ids = {facility.facility_id for facility in current_facilities}

    new_facility_ids = set(room_data.facilities_ids)
    facilities_to_add = new_facility_ids - current_facility_ids
    facilities_to_remove = current_facility_ids - new_facility_ids

    if facilities_to_remove:
        for facility_id in facilities_to_remove:
            await db.rooms_facilities.delete(room_id=room_id, facility_id=facility_id)

    if facilities_to_add:
        rooms_facilities_data = [
            RoomsFacilitiesAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()
    return {"status": 200}
