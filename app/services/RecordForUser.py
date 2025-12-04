from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import MakeRecord, RecordResponse, UserCreate, UserFind, RecordCreate, EditRecordStatus
from app.repositories import RecordRepository, UserRepository


async def user_create_record(
        record: MakeRecord,
        session: AsyncSession
) -> RecordResponse:
    async with session.begin():
        phone_number = record.phone_number
        user = await UserRepository.read_user_by_phone(session=session, user=UserFind(phone_number=phone_number))
        if not user:
            user = await UserRepository.create_user(session=session, user=UserCreate(phone_number=phone_number))
        created_record = RecordCreate(
            user_id=user.id,
            date=record.date,
            time=record.time,
            notes=record.notes,
        )
        created_record = await RecordRepository.create_record(session=session, record=created_record)
    return RecordResponse.model_validate(created_record)


async def user_find_record(
        user: UserFind,
        session: AsyncSession
) -> list[RecordResponse]:
    user = await UserRepository.read_user_by_phone(session=session, user=user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    records = await RecordRepository.read_record_by_user_id(session=session, user_id=user.id)
    return [RecordResponse.model_validate(record) for record in records]


async def switch_status_of_record(
        info_record: EditRecordStatus,
        session: AsyncSession,
) -> RecordResponse:
    async with session.begin():
        record = await RecordRepository.read_record_by_id(session=session, record_id=info_record.id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found"
            )
        updated_record = await RecordRepository.update_record_status(
            session=session,
            record=record,
            new_status=info_record.status,
        )
    return RecordResponse.model_validate(updated_record)

