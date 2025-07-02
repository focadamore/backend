from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None
):

    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from)
        .group_by(BookingsOrm.room_id)
    ).cte(name="rooms_count")

    rooms_free = (
        select(
            RoomsOrm.id.label("rooms_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked)).label("rooms_left")
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )

    get_rooms_in_hotel = (select(RoomsOrm.id).select_from(RoomsOrm))

    if hotel_id is not None:
        get_rooms_in_hotel = get_rooms_in_hotel.filter_by(hotel_id=hotel_id)

    get_rooms_in_hotel = get_rooms_in_hotel.subquery(name="get_rooms_in_hotel")

    rooms_ids_to_get = (
        select(rooms_free.c.rooms_id)
        .select_from(rooms_free)
        .filter(rooms_free.c.rooms_left > 0,
                rooms_free.c.rooms_id.in_(get_rooms_in_hotel)
                )
    )

    return rooms_ids_to_get
