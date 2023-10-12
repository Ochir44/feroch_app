from typing import Generator

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Creating an engine with a Postgres database URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
print("Database URL is ", SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Session database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """This dependence will using for connections to the database."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
