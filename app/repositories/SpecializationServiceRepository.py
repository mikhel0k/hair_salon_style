from typing import List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SpecializationService, Service


async def create_specialization_services(
        spec_service_data: List[SpecializationService],
        session: AsyncSession,
):
    session.add_all(spec_service_data)
    await session.flush()


async def read_services_by_specialization(
        specialization_id: int,
        session: AsyncSession,
):
    stmt = select(Service).join(SpecializationService).where(
        SpecializationService.specialization_id == specialization_id).order_by(
        SpecializationService.service_id.asc()
    )
    services = await session.execute(stmt)
    return services.scalars().all()


async def delete_connection(
        specialization_id: int,
        services: set[int],
        session: AsyncSession,
):
    stmt = delete(SpecializationService).where(
        SpecializationService.specialization_id == specialization_id,
        SpecializationService.service_id.in_(services)
    )
    await session.execute(stmt)

