from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Master import MasterResponse, MasterCreate
from app.services.MasterService import create_master

router = APIRouter()


@router.post("/new_master", response_model=MasterResponse)
async def new_master(
        master: MasterCreate,
        session: AsyncSession=Depends(get_session)
):
    return await create_master(session=session, master=master)