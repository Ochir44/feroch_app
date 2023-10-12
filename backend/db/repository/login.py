from db.models.users import Users
from sqlalchemy.orm import Session


async def get_user(username: str, db: Session):
    """Returns the user by email"""

    user = db.query(Users).filter(Users.email == username).first()
    return user
