from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.core import get_session
from app.schemas.Worker import WorkerCreate, Login
from app.services import AuthService

router = APIRouter()


@router.post("/registration")
async def registration(
        response: Response,
        worker: WorkerCreate,
        session: AsyncSession = Depends(get_session)
):
    token = await AuthService.registration(worker, session)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )
    return {"Created"}

@router.post("/login")
async def login(
        response: Response,
        login_data: Login,
        session: AsyncSession = Depends(get_session)
):
    token = await AuthService.login(login_data, session)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )
    return {"Login"}