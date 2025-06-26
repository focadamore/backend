from pydantic import BaseModel


class Hotels(BaseModel):
    title: str
    location: str


class HotelsPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
