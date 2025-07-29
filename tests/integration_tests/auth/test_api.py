import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@mail.ru", "12345", 200),
        ("testtwo@mail.ru", "12345", 200),
        ("test@mail.ru", "123456", 409),
        ("abcde", "1212121", 422),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_user_auth(email: str, password: str, status_code: int, ac: AsyncClient):
    # register
    response_register = await ac.post("/auth/register", json={"email": email, "password": password})
    assert response_register.status_code == status_code

    if response_register.status_code != 200:
        return

    # login
    await ac.post("/auth/login", json={"email": email, "password": password})
    assert "access_token" in ac.cookies
    assert ac.cookies["access_token"]

    # me
    response_me = await ac.get("/auth/me")
    assert response_me.json()["id"]
    assert response_me.json()["email"] == email
    assert "password" not in response_me.json()
    assert "hashed_password" not in response_me.json()

    # logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code

    # me_again
    response_me_logout = await ac.get("/auth/me")
    assert response_me_logout.status_code == 401
