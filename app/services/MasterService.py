from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Master
from app.schemas.Master import MasterCreate, MasterUpdate, MasterResponse, MasterFullResponse
from app.repositories import MasterRepository, ScheduleRepository
from app.schemas.Schedule import ScheduleCreate


async def create_master(
        master: MasterCreate,
        session: AsyncSession
):
    master = Master(**master.model_dump())
    try:
        master_in_db = await MasterRepository.create_master(master=master, session=session)
        await ScheduleRepository.create_schedule(ScheduleCreate(
            id=master_in_db.id,
            master_id=master_in_db.id
        ), session=session)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Master with this data already exists")
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
    try:
        master_in_db = await MasterRepository.update_master(master=master, session=session)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Master with this data already exists")
    return MasterResponse.model_validate(master_in_db)


async def get_master(
        master_id: int,
        session: AsyncSession
):
    master = await MasterRepository.read_master(master_id=master_id, session=session)
    if master is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Master not found")
    return MasterFullResponse.model_validate(master)


async def get_masters_by_service_id(
        service_id: int,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
):
    masters = await MasterRepository.read_masters_by_service_id(
        service_id=service_id,
        session=session,
        skip=skip,
        limit=limit,
    )
    return [MasterResponse.model_validate(master) for master in masters]
