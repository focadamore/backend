from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import Users


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = Users
