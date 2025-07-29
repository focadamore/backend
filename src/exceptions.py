from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Some Error Occurred. See log trace for details"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class UserNotFoundException(NabronirovalException):
    detail = "Пользователь не найден"


class RoomNotFoundException(NabronirovalException):
    detail = "Номер не найден"


class HotelNotFoundException(NabronirovalException):
    detail = "Номер не найден"


class IncorrectPasswordException(NabronirovalException):
    detail = "Некорректный пароль"


class NoFreeRoomsLeftException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Ошибка целостности данных (PK). Объект уже существует"


class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь уже существует"


class InvalidDatesRangeException(NabronirovalException):
    detail = "Дата заезда не может быть позже даты выезда"


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class UserNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Некорректный пароль"


class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже зарегистрирован"


class InvalidDatesRangeHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Дата заезда не может быть позже даты выезда"


class NoFreeRoomsLeftHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = "Не осталось свободных номеров"
