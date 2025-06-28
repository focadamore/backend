from pydantic import BaseModel


class HotelsAdd(BaseModel):
    title: str
    location: str


class Hotels(HotelsAdd):
    id: int


class HotelsPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
