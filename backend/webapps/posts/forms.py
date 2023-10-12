import os
from typing import List
from typing import Optional

from core.helpers import handle_file_upload
from db.models.posts import Post
from fastapi import File
from fastapi import Form
from fastapi import Request
from fastapi import UploadFile


class PostCreateForm:
    """This class will load and validate post_create form data."""

    def __init__(self, request: Request):
        """Initializing form data."""

        self.request: Request = request
        self.errors: list = []
        self.title: str = Form(...)
        self.text: str = Form(...)
        self.image: Optional[UploadFile] = File(None)

    async def load_data(self):
        """Load form data."""

        form = await self.request.form()
        self.title = form.get("title")
        self.text = form.get("text")
        self.image = form.get("image")

    async def is_valid(self):
        """Validate form data."""

        if self.image:
            # in this case, we separate the file name and format, and then check the format of the format.
            if os.path.splitext(self.image.filename)[1] not in (".png", ".jpg", ""):
                self.errors.append("Only .jpeg or .png  files allowed")
            else:
                self.image = await handle_file_upload(
                    self.image
                )  # Media file Processing
        if not self.errors:
            return True
        return False


class PostUpdateForm:
    """This class will load and validate post_update form data."""

    def __init__(self, request: Request):
        """Initializing form data."""

        self.request: Request = request
        self.errors: list = []
        self.title: str = Form(None)
        self.text: str = Form(None)
        self.image: Optional[UploadFile] = File(None)

    async def load_data(self):
        """Load form data."""

        form = await self.request.form()
        self.title = form.get("title")
        self.text = form.get("text")
        self.image = form.get("image")

    async def is_valid(self):
        """Validate form data."""
        if self.image:
            # in this case, we separate the file name and format, and then check the format of the format.
            if os.path.splitext(self.image.filename)[1] not in (".png", ".jpg", ""):
                self.errors.append("Only .jpeg or .png  files allowed")
            else:
                self.image = await handle_file_upload(
                    self.image
                )  # Media file Processing
        if not self.errors:
            return True
        return False
