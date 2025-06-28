from fastapi import APIRouter
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UsersRegisterAdd, UsersAdd


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", summary="Регистрация")
async def register_user(data: UsersRegisterAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {"status": 200}
