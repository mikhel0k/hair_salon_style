from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.schemas import RecordResponse, RecordCreate, RecordUpdate
from app.models import Record


async def create_record(
        record: RecordCreate,
        session: AsyncSession,
) -> RecordResponse:
    record_info = Record(**record.model_dump())
    session.add(record_info)
    await session.commit()
    await session.refresh(record_info)
    return RecordResponse.model_validate(record_info)


async def read_record_by_id(
        record_id: int,
        session: AsyncSession
) -> RecordResponse:
    record = await session.get(Record, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    return RecordResponse.model_validate(record)


async def read_record_by_user_id(
        user_id: int,
        session: AsyncSession
) -> list[RecordResponse]:
    stmt = select(Record).where(Record.user_id == user_id)
    result = await session.execute(stmt)
    records = result.scalars().all()
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    return [RecordResponse.model_validate(record) for record in records]
