from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas import MakeRecord, RecordResponse
from app.services import user_create_record


router = APIRouter()


@router.post("/create_record", response_model=RecordResponse)
async def create_record(
        record: MakeRecord,
        session: AsyncSession=Depends(get_session)
):
    return await user_create_record(session=session, record=record)