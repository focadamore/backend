from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Bookings
from src.schemas.facilities import Facilities
from src.schemas.hotels import Hotels
from src.schemas.rooms import Rooms
from src.schemas.users import Users


class HotelsDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotels


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = Users
