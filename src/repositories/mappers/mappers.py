from src.models.hotels import HotelsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotels


class HotelsDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotels
