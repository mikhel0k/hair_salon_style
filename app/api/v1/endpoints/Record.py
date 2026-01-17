from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.core.dependencies import is_user_master
from app.schemas.Record import EditRecordStatus, EditRecordNote, RecordUpdate, AllowedRecordStatuses
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
        record: RecordUpdate,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.update_record(
        record_id=record_id,
        data=record,
        session=session
    )


@router.put('/{record_id}/status/cancelled')
async def update_record_status_cancelled(
        record_id: int,
        session: AsyncSession = Depends(get_session)
):
    data = EditRecordStatus(
        id=record_id,
        status=AllowedRecordStatuses.Cancelled,
    )
    return await RecordService.update_status_to_cancelled(
        data=data,
        session=session
    )


@router.put('/{record_id}/status/confirmed')
async def update_record_status_confirmed(
        record_id: int,
        master = Depends(is_user_master),
        session: AsyncSession = Depends(get_session)
):
    data = EditRecordStatus(
        id=record_id,
        status=AllowedRecordStatuses.Confirmed,
    )
    return await RecordService.update_status_to_completed_or_confirmed(
        master_id=master["sub"],
        data=data,
        session=session
    )


@router.put('/{record_id}/status/completed')
async def update_record_status_completed(
        record_id: int,
        master = Depends(is_user_master),
        session: AsyncSession = Depends(get_session)
):
    data = EditRecordStatus(
        id=record_id,
        status=AllowedRecordStatuses.Completed,
    )
    return await RecordService.update_status_to_completed_or_confirmed(
        master_id=master["sub"],
        data=data,
        session=session
    )


@router.put('/{record_id}/note')
async def update_record_note(
        data: EditRecordNote,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.update_note_record(
        data=data,
        session=session
    )


@router.get("/master")
async def read_records_by_master_id_and_time_interval(
        start_time: date,
        master=Depends(is_user_master),
        end_time: date = None,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.read_records_by_master_id_and_time_interval(
        master_id=master["sub"],
        start_time=start_time,
        end_time=end_time,
        session=session
    )

