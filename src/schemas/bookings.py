from datetime import date

from pydantic import BaseModel


class BookingsAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingsAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Bookings(BookingsAdd):
    id: int


class BookingsPatchRequest(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    price: date | None = None


class BookingsPatch(BaseModel):
    user_id: int | None = None
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: date | None = None
