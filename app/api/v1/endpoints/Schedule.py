from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Schedule import ScheduleResponse, ScheduleUpdate
from app.services import ScheduleService

router = APIRouter()


@router.get("/master_id/{master_id}")
async def get_schedule_by_master_id(
        master_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await ScheduleService.get_schedule_by_master_id(master_id=master_id, session=session)


@router.patch("/{schedule_id}")
async def update_schedule(
        schedule_id: int,
        schedule: ScheduleUpdate,
        session: AsyncSession = Depends(get_session)
):
    return await ScheduleService.update_schedule(schedule_id=schedule_id, schedule_data=schedule, session=session)