import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.services import CellService

router = APIRouter()


@router.post("/{master_id}")
async def create_cells(
        master_id: int,
        session: AsyncSession=Depends(get_session)
):
    await CellService.make_cells(session=session, master_id=master_id)


@router.get("/")
async def read_cells(
        master_id: int,
        date: datetime.date,
        session: AsyncSession = Depends(get_session)
):
    return await CellService.get_cells_by_date_and_master_id(
        session=session,
        master_id=master_id,
        search_date=date
    )


@router.get("/free_days/service/{service_id}")
async def free_day_for_service(
        service_id: int,
        master_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await CellService.get_days_with_empty_cells_by_service_id_and_master_id(
        service_id=service_id,
        master_id=master_id,
        session=session
    )


@router.get("/free/service/{service_id}")
async def free_cells_for_service_in_date(
        date: datetime.date,
        service_id: int,
        master_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await CellService.get_days_with_empty_cells_by_service_id_master_id_and_date(
        record_date=date,
        service_id=service_id,
        master_id=master_id,
        session=session
    )
