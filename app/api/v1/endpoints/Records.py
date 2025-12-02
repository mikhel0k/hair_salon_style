from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas import MakeRecord, RecordResponse, UserFind, EditRecordStatus
from app.services import user_create_record, user_find_record, switch_status_of_record


router = APIRouter()


@router.post("/create_record", response_model=RecordResponse)
async def create_record(
        record: MakeRecord,
        session: AsyncSession=Depends(get_session)
):
    return await user_create_record(session=session, record=record)


@router.get("/records/{phone_number}", response_model=List[RecordResponse])
async def read_records(
        phone_number: str,
        session: AsyncSession = Depends(get_session)
):
    user = UserFind(phone_number=phone_number)
    return await user_find_record(session=session, user=user)


@router.patch("/status", response_model=RecordResponse)
async def update_record(
        record: EditRecordStatus,
        session: AsyncSession = Depends(get_session)
):
    return await switch_status_of_record(record, session)
