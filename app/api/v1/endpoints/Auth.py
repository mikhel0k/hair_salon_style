from fastapi import APIRouter, Depends, status
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.core import get_session, set_token
from app.core.redis import get_redis
from app.core.security import ACCESS_TOKEN_COOKIE_MAX_AGE, REFRESH_TOKEN_COOKIE_MAX_AGE
from app.core.dependencies import is_user_admin
from app.schemas.Worker import WorkerCreate, Login
from app.services import AuthService


router = APIRouter()


@router.post(
    "/registration/",
    status_code=status.HTTP_201_CREATED,
)
async def registration(
        worker_data: WorkerCreate,
        response: Response,
        admin_user=Depends(is_user_admin),
        session: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(get_redis),
):
    token, refresh_token = await AuthService.registration(
        worker_data=worker_data,
        session=session,
        redis_client=redis_client,
    )
    set_token(response, token, "access_token", ACCESS_TOKEN_COOKIE_MAX_AGE)
    set_token(response, refresh_token, "refresh_token", REFRESH_TOKEN_COOKIE_MAX_AGE)
    return {"status": "success"}


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
)
async def login(
        login_data: Login,
        response: Response,
        session: AsyncSession = Depends(get_session),
        redis_client: Redis = Depends(get_redis),
):
    token, refresh_token = await AuthService.login(
        login_data=login_data,
        session=session,
        redis_client=redis_client,
    )
    set_token(response, token, "access_token", ACCESS_TOKEN_COOKIE_MAX_AGE)
    set_token(response, refresh_token, "refresh_token", REFRESH_TOKEN_COOKIE_MAX_AGE)
    return {"status": "success"}
