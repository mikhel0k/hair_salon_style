from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.core import get_session, set_auth_token
from app.schemas.Worker import WorkerCreate, Login
from app.services import AuthService

router = APIRouter()


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
)
async def registration(
        worker_data: WorkerCreate,
        response: Response,
        session: AsyncSession = Depends(get_session)
):
    token = await AuthService.registration(
        worker_data=worker_data,
        session=session,
    )
    set_auth_token(response, token)
    return {"status": "success"}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
        login_data: Login,
        response: Response,
        session: AsyncSession = Depends(get_session)
):
    token = await AuthService.login(
        login_data=login_data,
        session=session,
    )
    set_auth_token(response, token)
    return {"status": "success"}
