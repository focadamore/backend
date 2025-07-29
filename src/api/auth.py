from fastapi import APIRouter, Response, Body

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserNotFoundException, UserNotFoundHTTPException, \
    IncorrectPasswordException, IncorrectPasswordHTTPException, UserAlreadyExistsHTTPException, \
    UserAlreadyExistsException
from src.schemas.users import UsersRegisterAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/login", summary="Аутентификация")
async def login_user(
        db: DBDep,
        response: Response,
        data: UsersRegisterAdd = Body(
            openapi_examples={
                "1": {"summary": "Я", "value": {"email": "me@mail.ru", "password": "123"}}
            }
        ),
):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register", summary="Регистрация")
async def register_user(data: UsersRegisterAdd, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": 200}


@router.get("/me", summary="тест Requests")
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await AuthService(db).get_me(user_id)
    return user


@router.post("/logout", summary="Выход из системы")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": 200}
