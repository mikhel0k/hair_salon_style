from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Worker import WorkerCreate
from app.services import AuthService

router = APIRouter()


@router.post("/registration")
async def registration(
        worker: WorkerCreate,
        session: AsyncSession = Depends(get_session)
):
    return await AuthService.registration(worker, session)