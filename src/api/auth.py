from fastapi import APIRouter, HTTPException, Response, Body

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UsersRegisterAdd, UsersAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/login", summary="Аутентификация")
async def login_user(
    response: Response,
    data: UsersRegisterAdd = Body(
        openapi_examples={
            "1": {"summary": "Я", "value": {"email": "me@mail.ru", "password": "123"}}
        }
    ),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не найден")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register", summary="Регистрация")
async def register_user(data: UsersRegisterAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except Exception:
            raise HTTPException(status_code=400)
        await session.commit()
        return {"status": 200}


@router.get("/me", summary="тест Requests")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user


@router.post("/logout", summary="Выход из системы")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": 200}
