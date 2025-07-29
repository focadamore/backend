from datetime import date

from src.exceptions import RoomNotFoundException, ObjectNotFoundException, HotelNotFoundException, \
    InvalidDatesRangeException
from src.schemas.facilities import RoomsFacilitiesAdd
from src.schemas.rooms import RoomsAddRequest, RoomsAdd, RoomsPatchRequest
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_rooms(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        try:
            rooms_data = await self.db.rooms.get_filtered_by_time(
                hotel_id=hotel_id,
                date_from=date_from,
                date_to=date_to
            )
        except InvalidDatesRangeException as ex:
            raise InvalidDatesRangeException from ex
        return rooms_data

    async def get_room(self, hotel_id: int, room_id: int):
        try:
            room_data = await self.db.rooms.get_one(room_id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        return room_data

    async def add_room(
            self,
            hotel_id: int,
            room_data: RoomsAddRequest
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        rooms_facilities_data = [
            RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        check_room_exists = self.db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
        return check_room_exists

    async def change_room(self, hotel_id: int, room_id: int, room_data: RoomsAddRequest):
        _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
        try:
            await self.db.rooms.get_one(id=room_id, data=_room_data)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        await self.db.rooms_facilities.delete(room_id=room_id)
        rooms_facilities_data = [
            RoomsFacilitiesAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

    async def change_room_partially(
        self, hotel_id: int, room_id: int, room_data: RoomsPatchRequest
    ):
        _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
        try:
            await self.db.rooms.edit(id=room_id, data=_room_data)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        current_facilities = await self.db.rooms_facilities.get_all(room_id=room_id)
        current_facility_ids = {facility.facility_id for facility in current_facilities}

        new_facility_ids = set(room_data.facilities_ids)
        facilities_to_add = new_facility_ids - current_facility_ids
        facilities_to_remove = current_facility_ids - new_facility_ids

        if facilities_to_remove:
            for facility_id in facilities_to_remove:
                await self.db.rooms_facilities.delete(room_id=room_id, facility_id=facility_id)

        if facilities_to_add:
            rooms_facilities_data = [
                RoomsFacilitiesAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()
