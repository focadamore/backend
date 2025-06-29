from pydantic import BaseModel


class RoomsAdd(BaseModel):
    title: str
    hotel_id: int
    description: str | None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomsPATCH(BaseModel):
    title: str | None
    hotel_id: int | None
    description: str | None
    price: int | None
    quantity: int | None
