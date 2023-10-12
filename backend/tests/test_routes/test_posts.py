import base64
from datetime import date
from datetime import datetime

import pytest
from core.helpers import handle_file_upload
from fastapi import File
from fastapi import status
from fastapi import UploadFile
from pydantic import BaseModel


class PostCreate(BaseModel):
    """Test schema PostCreate for tested post requests"""

    title: str | None = None
    text: str | None = None
    image: UploadFile = File(default=None)
    date_posted: date | None = datetime.now().date().strftime("%m-%d-%Y")


@pytest.mark.asyncio
async def test_create_post(client, normal_user_token_headers):
    """Create a post, tests status_code and verifies response with."""

    filename = "../backend/static/images/success.png"
    data = PostCreate(
        title="451",
        text="here not marketing",
    )
    response = client.post(
        "/posts/create-post/",
        data=data.dict(),
        files={"file": ("filename", open(filename, "rb"), "image/jpeg")},
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "451"
    assert response.json()["text"] == "here not marketing"


@pytest.mark.asyncio
async def test_read_post(client, normal_user_token_headers):
    """Create a post, then gets that post for reading and tests status_code."""

    filename = "../backend/static/images/success.png"
    data = PostCreate(title="451", text="here not marketing")
    # Since our tested functions are independent, we write post requests
    response = client.post(
        "/posts/create-post/",
        data=data.dict(),
        files={"file": ("filename", open(filename, "rb"), "image/jpeg")},
        headers=normal_user_token_headers,
    )
    response = client.get("/posts/get/1/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_posts(client, normal_user_token_headers):
    """Creates posts, then gets these posts for reading and tests status_code."""

    filename = "../backend/static/images/success.png"
    data = PostCreate(title="451", text="here not marketing")
    response = client.post(
        "/posts/create-post/",
        data=data.dict(),
        files={"file": ("filename", open(filename, "rb"), "image/jpeg")},
        headers=normal_user_token_headers,
    )
    response = client.post(
        "/posts/create-post/",
        data=data.dict(),
        files={"file": ("filename", open(filename, "rb"), "image/jpeg")},
        headers=normal_user_token_headers,
    )
    response = client.get("/posts/all-posts/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_post(client, normal_user_token_headers):
    """Create a post, then update data(data.title) and updating. Testing response form and status_code."""

    filename = "../backend/static/images/success.png"
    data = PostCreate(title="451", text="here not marketing")
    client.post(
        "/posts/create-post/",
        data=data.dict(),
        files={"file": ("filename", open(filename, "rb"), "image/jpeg")},
        headers=normal_user_token_headers,
    )
    data.title = "nft"
    response = client.post(
        "/posts/update-post/1", data=data.dict(), headers=normal_user_token_headers
    )
    assert response.json()["detail"] == "Successfully updated data."
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_post(client, normal_user_token_headers):
    """Create a post, then delete the post, then check the same post for its existence. Tesing status_code."""

    filename = "../backend/static/images/success.png"
    data = PostCreate(title="451", text="here not marketing")
    client.post(
        "/posts/create-post/",
        data=data.dict(),
        files={"file": ("filename", open(filename, "rb"), "image/jpeg")},
        headers=normal_user_token_headers,
    )
    msg = client.delete("/posts/delete/1", headers=normal_user_token_headers)
    response = client.get("/posts/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
