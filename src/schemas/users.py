from pydantic import BaseModel


class UsersRegisterAdd(BaseModel):
    email: str
    password: str


class UsersAdd(BaseModel):
    email: str
    hashed_password: str


class Users(BaseModel):
    id: int
    email: str
