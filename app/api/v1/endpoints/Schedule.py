from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_session
from app.schemas.Schedule import ScheduleUpdate, ScheduleResponse
from app.services import ScheduleService
from app.core.dependencies import is_user_master, is_user_admin

router = APIRouter()


def _require_master_id(master_data: dict) -> int:
    if master_data.get("master_id") is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Master profile not linked",
        )
    return master_data["master_id"]


@router.get(
    "/",
    response_model=ScheduleResponse,
    status_code=status.HTTP_200_OK,
)
async def get_schedule_by_master_id(
        master_data=Depends(is_user_master),
        session: AsyncSession = Depends(get_session),
):
    master_id = _require_master_id(master_data)
    return await ScheduleService.get_schedule_by_master_id(
        master_id=master_id,
        session=session,
    )


@router.patch(
    "/",
    response_model=ScheduleResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_schedule(
        schedule: ScheduleUpdate,
        master_data=Depends(is_user_master),
        session: AsyncSession = Depends(get_session),
):
    master_id = _require_master_id(master_data)
    return await ScheduleService.update_schedule(
        schedule_id=master_id,
        schedule_data=schedule,
        session=session,
    )


@router.get(
    "/{master_id}/",
    response_model=ScheduleResponse,
    status_code=status.HTTP_200_OK,
)
async def get_schedule_by_master_id_for_admin(
        master_id: int,
        admin_data=Depends(is_user_admin),
        session: AsyncSession = Depends(get_session),
):
    return await ScheduleService.get_schedule_by_master_id(
        master_id=master_id,
        session=session,
    )


@router.patch(
    "/{schedule_id}/",
    response_model=ScheduleResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_schedule_for_admin(
        schedule_id: int,
        schedule: ScheduleUpdate,
        admin_data=Depends(is_user_admin),
        session: AsyncSession = Depends(get_session),
):
    return await ScheduleService.update_schedule(
        schedule_id=schedule_id,
        schedule_data=schedule,
        session=session,
    )
