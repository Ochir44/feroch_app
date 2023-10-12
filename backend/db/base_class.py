from typing import Any

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr


@as_declarative()
class Base:
    # Creating id for each database
    id: Any
    __name__: str

    @declared_attr
    # to generate tablename from classname
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
