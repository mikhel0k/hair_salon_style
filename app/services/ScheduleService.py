import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ScheduleRepository
from app.schemas.Schedule import ScheduleResponse, ScheduleUpdate

logger = logging.getLogger(__name__)


async def get_schedule_by_master_id(
        master_id: int,
        session: AsyncSession
):
    schedule = await ScheduleRepository.read_schedule_by_master_id(
        master_id=master_id,
        session=session,
    )
    if schedule is None:
        logger.info("get_schedule_by_master_id: not found, master_id=%s", master_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )
    return ScheduleResponse.model_validate(schedule)


async def update_schedule(
        schedule_id: int,
        schedule_data: ScheduleUpdate,
        session: AsyncSession
):
    logger.debug("update_schedule: schedule_id=%s", schedule_id)
    schedule = await ScheduleRepository.read_schedule(
        schedule_id=schedule_id,
        session=session,
    )
    if schedule is None:
        logger.info("update_schedule: not found, schedule_id=%s", schedule_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )
    for key, value in schedule_data.model_dump(exclude_unset=True).items():
        setattr(schedule, key, value)
    try:
        schedule_in_db = await ScheduleRepository.update_schedule(
            schedule=schedule,
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("update_schedule: conflict, schedule_id=%s", schedule_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Schedule with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("update_schedule: unexpected error, schedule_id=%s", schedule_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Schedule updated: id=%s, master_id=%s", schedule_in_db.id, schedule_in_db.master_id)
    return ScheduleResponse.model_validate(schedule_in_db)
