from datetime import date

from sqlalchemy import select, between
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)
from app.models import Record, Cell


async def create_record(
        record: Record,
        session: AsyncSession,
) -> Record:
    session.add(record)
    await session.flush()
    await session.refresh(record)
    logger.info("Record created: id=%s, master_id=%s, service_id=%s, user_id=%s, cell_id=%s, status=%s", record.id, record.master_id, record.service_id, record.user_id, record.cell_id, record.status)
    return record


async def read_record_by_id(
        record_id: int,
        session: AsyncSession,
):
    record = await session.get(Record, record_id)
    logger.debug("Record read: id=%s, master_id=%s, service_id=%s, user_id=%s, cell_id=%s, status=%s", record.id, record.master_id, record.service_id, record.user_id, record.cell_id, record.status)
    return record


async def read_records_by_master_id(
        master_id: int,
        session: AsyncSession,
):
    stmt = select(Record).where(Record.master_id == master_id).order_by(Record.id.asc())
    records = await session.execute(stmt)
    logger.debug("Records read: %s", len(records.scalars().all()))
    return records.scalars().all()


async def read_records_by_master_id_and_time_interval(
        master_id: int,
        date_start: date,
        date_end: date,
        session: AsyncSession,
):
    stmt = select(Record).join(Cell).where(
        Record.master_id == master_id,
        between(Cell.date, date_start, date_end),
    ).order_by(Record.id.asc())
    records = await session.execute(stmt)
    logger.debug("Records read: %s", len(records.scalars().all()))
    return records.scalars().all()


async def read_records_by_servise_id(
        servise_id: int,
        session: AsyncSession,
):
    stmt = select(Record).where(Record.service_id == servise_id).order_by(Record.id.asc())
    records = await session.execute(stmt)
    logger.debug("Records read: %s", len(records.scalars().all()))
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
    logger.debug("Records read: %s", len(records.scalars().all()))
    return records.scalars().all()


async def read_record_by_cell_id(
        cell_id: int,
        session: AsyncSession,
):
    stmt = select(Record).where(Record.cell_id == cell_id)
    records = await session.execute(stmt)
    logger.debug("Records read: %s", len(records.scalars().all()))
    return records.scalars().all()


async def update_record(
        record: Record,
        session: AsyncSession,
):
    session.add(record)
    await session.flush()
    await session.refresh(record)
    logger.info("Record updated: id=%s, master_id=%s, service_id=%s, user_id=%s, cell_id=%s, status=%s", record.id, record.master_id, record.service_id, record.user_id, record.cell_id, record.status)
    return record
