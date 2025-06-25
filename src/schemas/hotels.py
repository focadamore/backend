from pydantic import BaseModel


class Hotels(BaseModel):
    title: str
    name: str


class HotelsPATCH(BaseModel):
    title: str | None = None
    name: str | None = None
