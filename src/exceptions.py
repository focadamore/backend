class NabronirovalException(Exception):
    detail = "Some Error Occurred. See log trace for details"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class NoFreeRoomsLeftException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Ошибка целостности данных (PK). Объект уже существует"


class InvalidDatesRangeException(NabronirovalException):
    detail = "Дата заезда не может быть позже даты выезда"
