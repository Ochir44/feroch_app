import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    """Create a user, testing status_code, his response(email and is_active)"""

    data = {
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
        "confirm_password": "testing",
    }
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True
