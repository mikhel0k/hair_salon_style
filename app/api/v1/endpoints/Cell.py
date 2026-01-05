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