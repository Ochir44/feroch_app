from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Post(Base):
    """Table for db - Post"""

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    image = Column(String, nullable=False)
    date_posted = Column(Date)
    is_active = Column(Boolean(), default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="posts")
