from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Master, Specialization
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


async def read_master(
        master_id: int,
        session: AsyncSession,
) -> Master | None:
    master = await session.get(Master, master_id)
    return master


async def read_masters_paginate(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Master).offset(skip).limit(limit).order_by(Master.id.desc())
    masters = await session.execute(stmt)
    return masters.scalars().all()


async def read_masters_by_category(
        session: AsyncSession,
        specialization: str,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Master).join(Specialization).where(Specialization.name == specialization).offset(skip).limit(limit)
    masters = await session.execute(stmt)
    return masters.scalars().all()


async def update_master(
        master: Master,
        session: AsyncSession,
):
    session.add(master)
    await session.commit()
    await session.refresh(master)
    return master
