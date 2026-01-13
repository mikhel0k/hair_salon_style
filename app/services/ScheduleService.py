from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ScheduleRepository
from app.schemas.Schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate


async def get_schedule_by_master_id(
        master_id: int,
        session: AsyncSession
):
    schedule = await ScheduleRepository.read_schedule_by_master_id(master_id=master_id, session=session)
    if schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return ScheduleResponse.model_validate(schedule)


async def update_schedule(
        schedule_id: int,
        schedule_data: ScheduleUpdate,
        session: AsyncSession
):
    schedule = await ScheduleRepository.read_schedule(schedule_id=schedule_id, session=session)
    if schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    for key, value in schedule_data.model_dump(exclude_unset=True).items():
        setattr(schedule, key, value)
    try:
        schedule_in_db = await ScheduleRepository.update_schedule(schedule=schedule, session=session)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Schedule with this data already exists")
    return ScheduleResponse.model_validate(schedule_in_db)
