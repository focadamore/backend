class NabronirovalException(Exception):
    detail = "Some Error Occurred. See log trace for details"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class NoFreeRoomsLeftException(NabronirovalException):
    detail = "Не осталось свободных номеров"
