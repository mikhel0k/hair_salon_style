from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Record


async def create_record(
        record: Record,
        session: AsyncSession,
) -> Record:
    session.add(record)
    await session.flush()
    await session.refresh(record)
    return record


async def read_record_by_id(
        record_id: int,
        session: AsyncSession,
):
    record = await session.get(Record, record_id)
    return record


async def read_records_by_master_id(
        master_id: int,
        session: AsyncSession,
):
    stmt = select(Record).where(Record.master_id == master_id).order_by(Record.id.asc())
    records = await session.execute(stmt)
    return records.scalars().all()


async def read_records_by_servise_id(
        servise_id: int,
        session: AsyncSession,
):
    stmt = select(Record).where(Record.service_id == servise_id).order_by(Record.id.asc())
    records = await session.execute(stmt)
    return records.scalars().all()


async def read_records_by_user_id(
        user_id: int,
        session: AsyncSession,
):
    stmt = select(Record).options(
        joinedload(Record.master),
        joinedload(Record.service),
        joinedload(Record.cell),
    ).where(Record.user_id == user_id).order_by(Record.id.asc())
    records = await session.execute(stmt)
    return records.scalars().all()


async def read_record_by_cell_id(
        cell_id: int,
        session: AsyncSession,
):
    stmt = select(Record).where(Record.cell_id == cell_id)
    records = await session.execute(stmt)
    return records.scalars().all()


async def update_record(
        record: Record,
        session: AsyncSession,
):
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record
