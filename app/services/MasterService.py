from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Master
from app.schemas.Master import MasterCreate, MasterUpdate, MasterResponse, MasterFullResponse
from app.repositories import MasterRepository


async def create_master(
        master: MasterCreate,
        session: AsyncSession
):
    master = Master(**master.model_dump())
    master_in_db = await MasterRepository.create_master(master=master, session=session)
    return MasterResponse.model_validate(master_in_db)


async def update_master(
        master_id: int,
        master_data: MasterUpdate,
        session: AsyncSession
):
    master = await MasterRepository.read_master(master_id=master_id, session=session)
    if master is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Master not found")
    for key, value in master_data.model_dump(exclude_unset=True).items():
        setattr(master, key, value)
    master_in_db = await MasterRepository.update_master(master=master, session=session)
    return MasterResponse.model_validate(master_in_db)


async def get_master(
        master_id: int,
        session: AsyncSession
):
    master = await MasterRepository.read_master(master_id=master_id, session=session)
    if master is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Master not found")
    return MasterFullResponse.model_validate(master)


async def get_masters_by_specialization_id(
        specialization_id: int,
        session: AsyncSession,
):
    masters = await MasterRepository.read_masters_by_specialization_id(specialization_id=specialization_id, session=session)
    return [MasterResponse.model_validate(master) for master in masters]
