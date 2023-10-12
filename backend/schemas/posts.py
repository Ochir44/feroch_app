from datetime import date
from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    """Shared properties."""

    title: str | None = None
    text: str | None = None
    image: str | None = None
    date_posted: date | None = datetime.now().date()


class PostCreate(PostBase):
    """Validate data when creating a post."""

    title: str | None = None
    text: str | None = None
    image: str | None = None


class UpdatePost(PostCreate):
    """Validate data when update a post."""

    pass


class ShowPost(PostBase):
    """This will be used to format the response to not to have id,owner_id etc."""

    title: str
    text: str
    image: str
    date_posted: date

    class Config:  # to convert non dict obj to json
        orm_mode = True
