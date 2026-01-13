from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Master import MasterResponse, MasterCreate, MasterUpdate
from app.services import MasterService


router = APIRouter()


@router.post("/", response_model=MasterResponse)
async def new_master(
        master: MasterCreate,
        session: AsyncSession=Depends(get_session)
):
    return await MasterService.create_master(master=master, session=session)


@router.get("/{master_id}")
async def get_master(
        master_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await MasterService.get_master(master_id=master_id, session=session)


@router.get("/by_service_id/{service_id}")
async def get_masters_by_service_id(
        service_id: int,
        session: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100
):
    return await MasterService.get_masters_by_service_id(
        service_id=service_id,
        session=session,
        skip=skip,
        limit=limit
    )


@router.patch("/{master_id}")
async def patch_master(
        master_id: int,
        update_master: MasterUpdate,
        session: AsyncSession = Depends(get_session),
):
    return await MasterService.update_master(master_id=master_id, master_data=update_master, session=session)
