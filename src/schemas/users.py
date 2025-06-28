from pydantic import BaseModel, EmailStr


class UsersRegisterAdd(BaseModel):
    email: EmailStr
    password: str


class UsersAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class Users(BaseModel):
    id: int
    email: EmailStr


class UsersWithHashedPassword(Users):
    hashed_password: str
