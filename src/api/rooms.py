from fastapi import Body, Query, APIRouter

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск отеля по id")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms",
            summary="Просмотр всех номеров отеля")
async def get_rooms(hotel_id: int,
                    title: str | None = Query(None, description="название номера"),
                    price: int | None = Query(None, description="цена за номер"),
                    ):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(title=title, price=price, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def add_room(hotel_id: int, room_data: RoomsAddRequest = Body(openapi_examples={
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
})
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
        return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {"status": 200}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение всех данных номера")
async def change_room(hotel_id: int, room_id: int, room_data: RoomsAddRequest):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            id=room_id,
            data=_room_data
        )
        await session.commit()
        return {"status": 200}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменение одного или нескольких тэгов номера")
async def change_room_partially(hotel_id: int, room_id: int, room_data: RoomsPatchRequest):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, hotel_id=hotel_id, exclude_unset=True, data=_room_data)
        await session.commit()
        return {"status": 200}
