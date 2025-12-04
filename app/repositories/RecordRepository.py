from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import RecordCreate
from app.models import Record


async def create_record(
        record: RecordCreate,
        session: AsyncSession,
) -> Record:
    record_info = Record(**record.model_dump())
    session.add(record_info)
    await session.flush()
    await session.refresh(record_info)
    return record_info


async def read_record_by_id(
        record_id: int,
        session: AsyncSession
) -> Record | None:
    return await session.get(Record, record_id)


async def read_record_by_user_id(
        user_id: int,
        session: AsyncSession
) -> Sequence[Record]:
    stmt = select(Record).where(Record.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_record_status(
        session: AsyncSession,
        record: Record,
        new_status: str,
):
    record.status = new_status
    await session.flush()
    await session.refresh(record)
    return record


async def update_record_note(
        session: AsyncSession,
        record: Record,
        new_note: str,
):
    record.notes = new_note
    await session.flush()
    await session.refresh(record)
    return record