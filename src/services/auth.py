from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone

from src.config import settings
from src.database import async_session_maker
from src.exceptions import ObjectAlreadyExistsException, UserNotFoundException, IncorrectPasswordException, \
    UserAlreadyExistsException
from src.repositories.users import UsersRepository
from src.schemas.users import UsersRegisterAdd, UsersAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=400, detail="Ошибка декодировки токена")

    async def login_user(
            self,
            data: UsersRegisterAdd
    ):
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
            if not user:
                raise UserNotFoundException
            if not AuthService().verify_password(data.password, user.hashed_password):
                raise IncorrectPasswordException
            access_token = AuthService().create_access_token({"user_id": user.id})
            return access_token

    async def register_user(self, data: UsersRegisterAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
        async with async_session_maker() as session:
            try:
                await UsersRepository(session).add(new_user_data)
            except ObjectAlreadyExistsException:
                raise UserAlreadyExistsException
            await session.commit()

    async def get_me(self, user_id: int):
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
