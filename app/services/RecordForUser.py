from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.schemas import MakeRecord, RecordResponse, UserCreate, UserFind, RecordCreate, EditRecordStatus, EditRecordNote
from app.repositories import RecordRepository, UserRepository


logger = logging.getLogger(__name__)


async def user_create_record(
        record: MakeRecord,
        session: AsyncSession
) -> RecordResponse:
    try:
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
    except HTTPException as e:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    except Exception as e:
        logger.error(f"System error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def user_find_record(
        user: UserFind,
        session: AsyncSession
) -> list[RecordResponse]:
    try:
        user = await UserRepository.read_user_by_phone(session=session, user=user)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        records = await RecordRepository.read_record_by_user_id(session=session, user_id=user.id)
        return [RecordResponse.model_validate(record) for record in records]
    except HTTPException as e:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    except Exception as e:
        logger.error(f"System error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def switch_status_of_record(
        info_record: EditRecordStatus,
        session: AsyncSession,
) -> RecordResponse:
    try:
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
    except HTTPException as e:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    except Exception as e:
        logger.error(f"System error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def change_note_of_record(
        info_record: EditRecordNote,
        session: AsyncSession,
):
    try:
        async with session.begin():
            record = await RecordRepository.read_record_by_id(session=session, record_id=info_record.id)
            if not record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Record not found"
                )
            updated_record = await RecordRepository.update_record_note(
                session=session,
                record=record,
                new_note=info_record.notes,
            )
            return RecordResponse.model_validate(updated_record)
    except HTTPException as e:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    except Exception as e:
        logger.error(f"System error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
