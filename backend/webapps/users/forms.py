from typing import List
from typing import Optional

from fastapi import Request
from pydantic import EmailStr


class UserCreateForm:
    """Class will accept and validate form data"""

    def __init__(self, request: Request):
        """Initializing form data"""

        self.request: Request = request
        self.errors: list = []
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.confirm_password: Optional[str] = None

    async def load_data(self):
        """Load form data."""

        form = await self.request.form()
        self.username = form.get("username")
        self.email = form.get("email")
        self.password = form.get("password")
        self.confirm_password = form.get("confirm_password")

    async def is_valid(self):
        """Validate form data"""

        if not self.username or not len(self.username) > 3:
            self.errors.append("Username should be > 3 chars")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be > 4 chars")
        if self.password != self.confirm_password:
            self.errors.append("Passwords don't match")
        if not self.errors:
            return True
        return False
