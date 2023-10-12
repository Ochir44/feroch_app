from core.hashing import Hasher
from db.models.users import Users
from schemas.users import UserCreate
from sqlalchemy.orm import Session


async def create_new_user(user: UserCreate, db: Session):
    """Database write new user in User model and return result"""
    user = Users(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_user_by_email(email: str, db: Session):
    """Database find user by email and return result"""

    user = db.query(Users).filter(Users.email == email).first()
    return user
