from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.UserFlow import MakeRecord
from app.services import RecordService

router = APIRouter()


@router.post('/new_record')
async def new_record(
        record: MakeRecord,
        session: AsyncSession = Depends(get_session)
):
    return await RecordService.new_record(session=session, data=record)