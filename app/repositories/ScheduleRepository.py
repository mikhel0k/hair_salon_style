from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    return schedule


async def read_schedule(
        schedule_id: int,
        session: AsyncSession
):
    schedule = await session.get(Schedule, schedule_id)
    return schedule


async def read_schedule_by_master_id(
        master_id: int,
        session: AsyncSession
):
    stmt = select(Schedule).where(Schedule.master_id == master_id).order_by(Schedule.id.asc())
    schedule = await session.execute(stmt)
    return schedule.scalar_one_or_none()


async def update_schedule(
        schedule: Schedule,
        session: AsyncSession
):
    session.add(schedule)
    await session.flush()
    await session.refresh(schedule)
    return schedule


async def delete_schedule(
        schedule: Schedule,
        session: AsyncSession,
):
    await session.delete(schedule)
    await session.flush()
