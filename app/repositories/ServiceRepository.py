from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Service
from app.schemas.Service import ServiceCreate


async def create_service(
        service: ServiceCreate,
        session: AsyncSession,
) -> Service:
    service = Service(**service.model_dump())
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


async def read_service_by_id(
        service_id: int,
        session: AsyncSession
):
    service = await session.get(Service, service_id)
    return service


async def read_services_by_category_id(
        category_id: int,
        session: AsyncSession
):
    stmt = select(Service).where(Service.category_id == category_id).order_by(Service.category_id.desc())
    services = await session.execute(stmt)
    return services.scalars().all()


async def update_service(
        service: Service,
        session: AsyncSession,
):
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


async def delete_service(
        service: Service,
        session: AsyncSession,
):
    await session.delete(service)
    await session.commit()
