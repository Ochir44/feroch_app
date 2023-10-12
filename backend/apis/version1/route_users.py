from db.repository.users import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from schemas.users import ShowUser
from schemas.users import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=ShowUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """create_user function will receive user from request and UserCreate schema
    will validate that it has a username,email in proper format, and a password.
    """

    user = await create_new_user(user=user, db=db)
    return user
