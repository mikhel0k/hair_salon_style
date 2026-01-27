from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

from app.core.security import decode_token


async def get_worker(
        request: Request,
):
    token = request.cookies.get("access_token")
    print(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        data = decode_token(token)
        try:
            master_id = int(data.get("master_id"))
        except Exception as e:
            print(e)
            master_id = None
        return {
            "sub": int(data.get("sub")),
            "master_id": master_id,
            "is_master": data.get("is_master"),
            "is_admin": data.get("is_admin"),
            "is_active": data.get("is_active"),
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid parsing")


async def is_user_master(data: dict = Depends(get_worker)):
    if not data["is_master"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return data


async def is_user_admin(data: dict = Depends(get_worker)):
    if not data["is_admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not data["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return data
