from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
import jwt

from settings import settings
from starlette.responses import Response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_PRIVATE_KEY = settings.JWT_PRIVATE_KEY.read_text()
JWT_PUBLIC_KEY = settings.JWT_PUBLIC_KEY.read_text()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data_dict: dict) -> str:
    data = data_dict.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_PRIVATE_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM,])


def set_auth_token(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=1800
    )