from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Specialization
from app.schemas.Specialization import SpecializationCreate


async def create_specialization(
        service_data: SpecializationCreate,
        session: AsyncSession,
) -> Specialization:
    specialization = Specialization(**service_data.model_dump())
    session.add(specialization)
    await session.commit()
    await session.refresh(specialization)
    return specialization


async def read_specialization(
        specialization_id: int,
        session: AsyncSession,
):
    specialization = await session.get(Specialization, specialization_id)
    return specialization


async def delete_specialization(
        specialization: Specialization,
        session: AsyncSession,
):
    await session.delete(specialization)
    await session.commit()
