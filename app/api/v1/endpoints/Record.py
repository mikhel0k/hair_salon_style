from faker.providers import phone_number
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Record import EditRecordStatus, EditRecordNote
from app.schemas.UserFlow import MakeRecord
from app.schemas.User import UserFind
from app.services import RecordService

router = APIRouter()


@router.post('/')
async def create_record(
        record: MakeRecord,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.new_record(session=session, data=record)


@router.get('/phone_number')
async def get_records_hy_phone(
        phone_number: str,
        session: AsyncSession = Depends(get_session)
):
    user = UserFind(phone_number=phone_number)
    return await RecordService.get_records_hy_phone(
        user=user,
        session=session
    )


@router.patch('/{record_id}')
async def update_record(
        record_id: int,
        record: MakeRecord,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.update_record(
        record_id=record_id,
        data=record,
        session=session
    )


@router.put('/{record_id}/status/{new_status}')
async def update_record_status(
        data: EditRecordStatus,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.update_status_record(
        data=data,
        session=session
    )


@router.put('/{record_id}/note/{new_status}')
async def update_record_note(
        data: EditRecordNote,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.update_note_record(
        data=data,
        session=session
    )

