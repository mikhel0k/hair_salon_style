from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import logging

logger = logging.getLogger(__name__)
from app.models import Specialization, Service
from app.schemas.Specialization import SpecializationCreate


async def create_specialization(
        specialization_data: SpecializationCreate,
        session: AsyncSession,
) -> Specialization:
    specialization = Specialization(**specialization_data.model_dump())
    session.add(specialization)
    await session.flush()
    await session.refresh(specialization)
    logger.info("Specialization created: id=%s, name=%s", specialization.id, specialization.name)
    return specialization


async def read_specialization(
        specialization_id: int,
        session: AsyncSession,
):
    stmt = select(Specialization).options(selectinload(Specialization.services)).where(Specialization.id == specialization_id)
    specialization = await session.execute(stmt)
    logger.debug("Specialization read: id=%s, name=%s", specialization.id, specialization.name)
    return specialization.scalars().one_or_none()


async def read_specializations(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Specialization).offset(skip).limit(limit)
    specializations = await session.execute(stmt)
    logger.debug("Specializations read: %s", len(specializations.scalars().all()))
    return specializations.scalars().all()
