from fastapi import HTTPException, Depends
from starlette import status
from starlette.responses import Response
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token, ACCESS_TOKEN_COOKIE_MAX_AGE, REFRESH_TOKEN_COOKIE_MAX_AGE
from app.services import AuthService
from app.core.database import get_session
from app.core import set_token
from app.core.redis import get_redis


async def get_worker(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_session),
):
    token = request.cookies.get("access_token")
    if not token:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        try:
            data = decode_token(refresh_token)
            user_id = data.get("sub")
            jti = data.get("jti")
            if not user_id or not jti:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            redis_client = get_redis()
            redis_key = f"refresh_token:{user_id}:{jti}"
            if not redis_client.exists(redis_key):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token revoked or expired",
                )
            token = await AuthService.get_new_access_token(
                data=data,
                session=session,
            )
            set_token(response, token, "access_token", ACCESS_TOKEN_COOKIE_MAX_AGE)
            set_token(response, refresh_token, "refresh_token", REFRESH_TOKEN_COOKIE_MAX_AGE)
            decoded = decode_token(token)
            try:
                master_id = int(decoded.get("master_id"))
            except (TypeError, ValueError):
                master_id = None
            return {
                "sub": int(decoded.get("sub")),
                "master_id": master_id,
                "is_master": decoded.get("is_master"),
                "is_admin": decoded.get("is_admin"),
                "is_active": decoded.get("is_active"),
            }
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid parsing")
    else:
        try:
            data = decode_token(token)
            try:
                master_id = int(data.get("master_id"))
            except (TypeError, ValueError):
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
