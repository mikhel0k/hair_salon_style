from typing import List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)
from app.models import SpecializationService, Service


async def create_specialization_services(
        spec_service_data: List[SpecializationService],
        session: AsyncSession,
):
    session.add_all(spec_service_data)
    await session.flush()
    logger.info("Specialization services created: %s", len(spec_service_data))


async def read_services_by_specialization(
        specialization_id: int,
        session: AsyncSession,
):
    stmt = select(Service).join(SpecializationService).where(
        SpecializationService.specialization_id == specialization_id).order_by(
        SpecializationService.service_id.asc()
    )
    services = await session.execute(stmt)
    logger.debug("Services read: %s", len(services.scalars().all()))
    return services.scalars().all()


async def delete_connection(
        specialization_id: int,
        services: set[int],
        session: AsyncSession,
):  
    logger.info("Specialization services deleted: %s", len(services))
    stmt = delete(SpecializationService).where(
        SpecializationService.specialization_id == specialization_id,
        SpecializationService.service_id.in_(services)
    )
    await session.execute(stmt)

