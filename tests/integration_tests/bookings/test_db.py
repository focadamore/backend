from datetime import date

from src.schemas.bookings import BookingsAdd, BookingsPatchRequest


async def test_booking_crud(db):
    # CREATE
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=7, day=20),
        date_to=date(year=2025, month=7, day=30),
        price=10000,
    )
    new_booking = await db.bookings.add(booking_data)
    await db.commit()
    print(f"{new_booking=}")

    # READ
    check_read = await db.bookings.get_one_or_none(id=new_booking.id)
    print(f"{check_read=}")
    assert check_read == new_booking

    # UPDATE
    booking_update_data = BookingsPatchRequest(
        date_from=date(year=2025, month=7, day=20),
        date_to=date(year=2025, month=7, day=30),
        price=5000,
    )
    await db.bookings.edit(booking_update_data, user_id=user_id, room_id=room_id)
    await db.commit()
    check_update = await db.bookings.get_one_or_none(id=new_booking.id)

    booking_update_data = booking_update_data.model_dump()
    check_update = check_update.model_dump()
    for k in booking_update_data:
        assert booking_update_data[k] == check_update[k]

    # DELETE
    await db.bookings.delete(user_id=user_id, room_id=room_id)
    check_delete = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert not check_delete
