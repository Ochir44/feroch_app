from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    """Properties required during user creation"""

    username: str
    email: EmailStr
    password: str
    confirm_password: str


class ShowUser(BaseModel):
    """This will be used to format the response to not to have id,owner_id etc."""

    username: str
    email: EmailStr
    is_active: bool

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True
