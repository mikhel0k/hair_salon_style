from phonenumbers.unicode_util import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Service
from app.schemas.Service import ServiceCreate, ServiceUpdate


async def create_service(
        service: ServiceCreate,
        session: AsyncSession,
) -> Service:
    service_info = Service(**service.model_dump())
    session.add(service_info)
    await session.commit()
    await session.refresh(service_info)
    return service_info


async def get_services(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Service).offset(skip).limit(limit)
    result = await session.execute(stmt)
    services = result.scalars().all()
    return services


async def get_services_by_category(
        session: AsyncSession,
        category: str,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Service).where(Service.category == category).offset(skip).limit(limit)
    result = await session.execute(stmt)
    services = result.scalars().all()
    return services

async def update_service_by_id(
        service_id: int,
        service: ServiceUpdate,
        session: AsyncSession,
):
    stmt = select(Service).where(Service.id == service_id)
    result = await session.execute(stmt)
    service_info = result.scalar_one_or_none()
    for key, value in service.model_dump().items():
        if value is not None:
            setattr(service_info, key, value)
    await session.commit()
    await session.refresh(service_info)
    return service_info

async def delete_service_by_id(
        service_id: int,
        session: AsyncSession,
):
    stmt = select(Service).where(Service.id == service_id)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()
    result.description = "cancelled"
    await session.commit()