from datetime import datetime, timedelta, timezone
import logging

import bcrypt
import jwt

from settings import settings
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Токены: duration в минутах, max_age для cookie в секундах
ACCESS_TOKEN_DURATION_MIN = 30
REFRESH_TOKEN_DURATION_MIN = 30 * 24 * 60  # 30 дней
ACCESS_TOKEN_COOKIE_MAX_AGE = 30 * 60  # 30 мин в секундах
REFRESH_TOKEN_COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 дней в секундах

JWT_PRIVATE_KEY = settings.JWT_PRIVATE_KEY.read_text()
JWT_PUBLIC_KEY = settings.JWT_PUBLIC_KEY.read_text()


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_token(data_dict: dict, duration: int = 30) -> str:
    data = data_dict.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=duration)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_PRIVATE_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM,])


def set_token(response: Response, token: str, key: str, max_age: int):
    response.set_cookie(
        key=key,
        value=token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=max_age
    )