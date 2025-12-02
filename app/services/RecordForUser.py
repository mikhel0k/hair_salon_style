from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import MakeRecord, RecordResponse, UserCreate, UserFind, RecordCreate
from app.repositories import RecordRepository, UserRepository



async def user_create_record(
        record: MakeRecord,
        session: AsyncSession
) -> RecordResponse:
    phone_number = record.phone_number
    user = await UserRepository.read_user_by_phone(session=session, user=UserFind(phone_number=phone_number))
    if not user:
        user = await UserRepository.create_user(session=session, user=UserCreate(phone_number=phone_number))
    created_record = RecordCreate(
        user_id=user.id,
        date=record.date,
        time=record.time,
    )
    return await RecordRepository.create_record(session=session, record=created_record)


async def user_find_record(
        user: UserFind,
        session: AsyncSession
) -> list[RecordResponse]:
    phone_number = user.phone_number
    user = await UserRepository.read_user_by_phone(session=session, user=user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    records = await RecordRepository.read_record_by_user_id(session=session, user_id=user.id)
    return records
