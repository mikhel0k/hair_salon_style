from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Service
from app.schemas.Service import ServiceCreate


async def create_service(
        service: ServiceCreate,
        session: AsyncSession,
) -> Service:
    master_info = Service(**service.model_dump())
    session.add(master_info)
    await session.commit()
    await session.refresh(master_info)
    return master_info
