from passlib.context import CryptContext
import jwt

from settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data_dict: dict):
    return jwt.encode(data_dict, settings.JWT_PRIVATE_KEY.read_text(), algorithm=settings.ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, settings.JWT_PUBLIC_KEY.read_text(), algorithms=[settings.ALGORITHM,])
