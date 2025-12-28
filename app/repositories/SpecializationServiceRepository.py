from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SpecializationService


async def create_specialization_service(
        specialization_id: int,
        service_id: int,
        session: AsyncSession,
):
    spec_service = SpecializationService(
        specialization_id=specialization_id,
        service_id=service_id,
    )
    session.add(spec_service)
    await session.commit()
    await session.refresh(spec_service)
    return spec_service


async def get_services_by_specialization(
        specialization_id: int,
        session: AsyncSession,
):
    stmt = select(SpecializationService).where(SpecializationService.specialization_id == specialization_id)
    services = await session.execute(stmt)
    return services.scalars().all()


async def get_specializations_by_service(
        service_id: int,
        session: AsyncSession,
):
    stmt = select(SpecializationService).where(SpecializationService.service_id == service_id)
    specializations = await session.execute(stmt)
    return specializations.scalars().all()


async def get_specialization_and_service_id(
        specialization_service_id: int,
        session: AsyncSession,
):
    spec_service = await session.get(SpecializationService, specialization_service_id)
    return spec_service


async def delete_connection(
        spec_service: SpecializationService,
        session: AsyncSession,
):
    await session.delete(spec_service)
    await session.commit()
