from datetime import timedelta

from apis.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.repository.login import get_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from schemas.tokens import Token
from sqlalchemy.orm import Session


router = APIRouter()


async def authenticate_user(username: str, password: str, db: Session):
    """Getting username and password for authenticate"""

    user = await get_user(username=username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """The function accepts the response parameter for the  set cookie parameter, form_data for authenticate_user and db."""

    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_TOKEN)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )  # set HttpOnly cookie in response
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/login/token"
)  # changed to use our implementation


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """This function works as a dependency"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        # decoding the token if it is present and we are validating the user. Once we have a user, we are simply returning it.
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user
