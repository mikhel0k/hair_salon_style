from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Master, SpecializationService


async def create_master(
        master: Master,
        session: AsyncSession,
) -> Master:
    session.add(master)
    await session.commit()
    await session.refresh(master)
    return master


async def read_master(
        master_id: int,
        session: AsyncSession,
) -> Master | None:
    stmt = select(Master).options(joinedload(Master.specialization)).where(Master.id == master_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def read_masters_by_service_id(
    session: AsyncSession,
    service_id: int,
    skip: int = 0,
    limit: int = 100,
):
    stmt = (
        select(Master)
        .join(Master.specialization)
        .join(SpecializationService, SpecializationService.specialization_id == Master.specialization_id)
        .where(SpecializationService.service_id == service_id)
        .offset(skip).limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_master(
        master: Master,
        session: AsyncSession,
):
    session.add(master)
    await session.commit()
    await session.refresh(master)
    return master
