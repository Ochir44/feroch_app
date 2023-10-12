from typing import List
from typing import Optional

from fastapi import Request


class LoginForm:
    """A class that will act as a form validator"""

    def __init__(self, request: Request):
        """Initializing form data"""

        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        """Load form data."""

        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        """Validate form data"""

        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
