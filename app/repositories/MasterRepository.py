from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)
from app.models import Master, SpecializationService, Specialization


async def create_master(
        master: Master,
        session: AsyncSession,
) -> Master:
    session.add(master)
    await session.flush()
    await session.refresh(master)
    logger.info("Master created: id=%s, specialization_id=%s, name=%s, phone=%s, email=%s, status=%s", master.id, master.specialization_id, master.name, master.phone, master.email, master.status)
    return master


async def read_masters(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Master).options(joinedload(Master.specialization)).offset(skip).limit(limit)
    result = await session.execute(stmt)
    logger.debug("Masters read: %s", len(result.scalars().all()))
    return result.scalars().all()


async def read_master(
        master_id: int,
        session: AsyncSession,
):
    master = await session.get(Master, master_id)
    logger.debug("Master read: id=%s, specialization_id=%s, name=%s, phone=%s, email=%s, status=%s", master.id, master.specialization_id, master.name, master.phone, master.email, master.status)
    return master


async def read_masters_by_service_id(
    session: AsyncSession,
    service_id: int,
    skip: int = 0,
    limit: int = 100,
):
    stmt = (
        select(Master)

        .join(Specialization)
        .join(SpecializationService)
        .where(SpecializationService.service_id == service_id)
        .offset(skip).limit(limit)
    )
    result = await session.execute(stmt)
    logger.debug("Masters read: %s", len(result.scalars().all()))
    return result.scalars().all()


async def checking_master_provides_service(
        master_id: int,
        service_id: int,
        session: AsyncSession,
):
    query = (
        select(Master)
        .join(Specialization)
        .join(SpecializationService)
        .where(Master.id == master_id)
        .where(SpecializationService.service_id == service_id)
    )
    stmt = select(query.exists())
    result = await session.execute(stmt)
    logger.debug("Master provides service: %s", result.scalar() or False)
    return result.scalar() or False


async def update_master(
        master: Master,
        session: AsyncSession,
):
    session.add(master)
    await session.flush()
    await session.refresh(master)
    logger.info("Master updated: id=%s, specialization_id=%s, name=%s, phone=%s, email=%s, status=%s", master.id, master.specialization_id, master.name, master.phone, master.email, master.status)
    return master
