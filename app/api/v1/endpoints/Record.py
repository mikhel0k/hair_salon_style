from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_session
from app.core.dependencies import is_user_master
from app.schemas.Record import EditRecordStatus, EditRecordNote, RecordUpdate, AllowedRecordStatuses, RecordResponse
from app.schemas.UserFlow import MakeRecord
from app.schemas.User import UserFind
from app.services import RecordService

router = APIRouter()


@router.post(
    "/",
    response_model=RecordResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_record(
        record_data: MakeRecord,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.new_record(
        session=session,
        data=record_data
    )


@router.get(
    "/by-phone/{phone_number}/",
    response_model=list[RecordResponse],
    status_code=status.HTTP_200_OK,
)
async def get_records_by_phone(
        phone_number: str,
        session: AsyncSession = Depends(get_session)
):
    user = UserFind(phone_number=phone_number)
    return await RecordService.get_records_by_phone(
        user=user,
        session=session
    )


@router.patch(
    "/{record_id}/",
    response_model=RecordResponse,
    status_code=status.HTTP_200_OK,
)
async def update_record(
        record_id: int,
        record_data: RecordUpdate,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.update_record(
        record_id=record_id,
        data=record_data,
        session=session
    )


@router.put(
    "/{record_id}/status/cancelled/",
    response_model=RecordResponse,
    status_code=status.HTTP_200_OK,
)
async def update_record_status_cancelled(
        record_id: int,
        session: AsyncSession = Depends(get_session)
):
    data = EditRecordStatus(
        id=record_id,
        status=AllowedRecordStatuses.CANCELLED,
    )
    return await RecordService.update_status_to_cancelled(
        data=data,
        session=session
    )


@router.put(
    "/{record_id}/status/confirmed/",
    response_model=RecordResponse,
    status_code=status.HTTP_200_OK,
)
async def update_record_status_confirmed(
        record_id: int,
        master_data = Depends(is_user_master),
        session: AsyncSession = Depends(get_session)
):
    data = EditRecordStatus(
        id=record_id,
        status=AllowedRecordStatuses.CONFIRMED,
    )
    return await RecordService.update_status_to_completed_or_confirmed(
        master_id=master_data["sub"],
        data=data,
        session=session
    )


@router.put(
    "/{record_id}/status/completed/",
    response_model=RecordResponse,
    status_code=status.HTTP_200_OK,
)
async def update_record_status_completed(
        record_id: int,
        master_data = Depends(is_user_master),
        session: AsyncSession = Depends(get_session)
):
    data = EditRecordStatus(
        id=record_id,
        status=AllowedRecordStatuses.COMPLETED,
    )
    return await RecordService.update_status_to_completed_or_confirmed(
        master_id=master_data["sub"],
        data=data,
        session=session
    )


@router.put(
    "/{record_id}/note/",
    response_model=RecordResponse,
    status_code=status.HTTP_200_OK,
)
async def update_record_note(
        record_data: EditRecordNote,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.update_note_record(
        data=record_data,
        session=session
    )


@router.get(
    "/master/",
    response_model=list[RecordResponse],
    status_code=status.HTTP_200_OK,
)
async def read_records_by_master_id_and_time_interval(
        start_time: date,
        end_time: date=None,
        master_data=Depends(is_user_master),
        session: AsyncSession=Depends(get_session)
):
    return await RecordService.read_records_by_master_id_and_time_interval(
        master_id=master_data["sub"],
        start_time=start_time,
        end_time=end_time,
        session=session
    )
