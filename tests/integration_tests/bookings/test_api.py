async def test_add_booking(authenticated_ac, db):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-12-12",
            "date_to": "2025-01-01"
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert "data" in res
    assert res["status"] == "OK"
