from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Master
from app.schemas.Master import MasterCreate


async def create_master(
        master: MasterCreate,
        session: AsyncSession,
) -> Master:
    master_info = Master(**master.model_dump())
    session.add(master_info)
    await session.commit()
    await session.refresh(master_info)
    return master_info
