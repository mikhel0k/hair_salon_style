from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)
from app.models import Schedule
from app.schemas.Schedule import ScheduleCreate


async def create_schedule(
        schedule_data: ScheduleCreate,
        session: AsyncSession,
) -> Schedule:
    schedule = Schedule(**schedule_data.model_dump())
    session.add(schedule)
    await session.flush()
    await session.refresh(schedule)
    logger.info("Schedule created: id=%s, master_id=%s, date=%s, time=%s, status=%s", schedule.id, schedule.master_id, schedule.date, schedule.time, schedule.status)
    return schedule


async def read_schedule(
        schedule_id: int,
        session: AsyncSession
):
    schedule = await session.get(Schedule, schedule_id)
    logger.debug("Schedule read: id=%s, master_id=%s, date=%s, time=%s, status=%s", schedule.id, schedule.master_id, schedule.date, schedule.time, schedule.status)
    return schedule


async def read_schedule_by_master_id(
        master_id: int,
        session: AsyncSession
):
    stmt = select(Schedule).where(Schedule.master_id == master_id).order_by(Schedule.id.asc())
    schedule = await session.execute(stmt)
    logger.debug("Schedule read: %s", len(schedule.scalars().all()))
    return schedule.scalar_one_or_none()


async def update_schedule(
        schedule: Schedule,
        session: AsyncSession
):
    session.add(schedule)
    await session.flush()
    await session.refresh(schedule)
    logger.info("Schedule updated: id=%s, master_id=%s, date=%s, time=%s, status=%s", schedule.id, schedule.master_id, schedule.date, schedule.time, schedule.status)
    return schedule
