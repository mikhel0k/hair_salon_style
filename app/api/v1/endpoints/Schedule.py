from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Schedule import ScheduleUpdate
from app.services import ScheduleService
from app.core.dependencies import is_user_master

router = APIRouter()


@router.get("/")
async def get_schedule_by_master_id(
        master=Depends(is_user_master),
        session: AsyncSession = Depends(get_session)
):
    return await ScheduleService.get_schedule_by_master_id(master_id=master["sub"], session=session)


@router.patch("/")
async def update_schedule(
        schedule: ScheduleUpdate,
        master=Depends(is_user_master),
        session: AsyncSession = Depends(get_session)
):
    return await ScheduleService.update_schedule(schedule_id=master["sub"], schedule_data=schedule, session=session)