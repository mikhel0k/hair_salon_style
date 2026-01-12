from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

from app.core.security import decode_token


async def get_worker(
        request: Request,
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        data = decode_token(token)
        return {
            "id": data.get("sub"),
            "is_master": data.get("is_master"),
            "is_admin": data.get("is_admin"),
            "is_active": data.get("is_active"),
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def is_user_master(data: dict = Depends(get_worker)):
    if not data["is_master"] and not data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return data


async def is_user_admin(data: dict = Depends(get_worker)):
    if not data["is_admin"] and not data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return data
