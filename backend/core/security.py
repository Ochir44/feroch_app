from datetime import datetime
from datetime import timedelta

from core.config import settings
from jose import jwt
from jose import JWTError


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Getting a data dictionary with subject(sub) and parametr for token exparation date"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES_TOKEN
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
