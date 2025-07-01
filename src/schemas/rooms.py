from pydantic import BaseModel


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None


class RoomsAdd(BaseModel):
    title: str
    hotel_id: int
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomsPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None


class RoomsPatch(BaseModel):
    title: str | None = None
    hotel_id: int | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
