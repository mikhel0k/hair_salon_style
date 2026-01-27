import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.core.dependencies import is_user_admin
from app.schemas.Cell import CellResponse
from app.services import CellService

router = APIRouter()


@router.post(
    "/{master_id}",
    response_model=dict[str, str],
    status_code=status.HTTP_201_CREATED,
)
async def create_cells(
        master_id: int,
        admin_user = Depends(is_user_admin),
        session: AsyncSession=Depends(get_session)
):
    await CellService.make_cells(
        session=session,
        master_id=master_id
    )
    return {"status": "success"}


@router.get(
    "/",
    response_model=list[CellResponse],
    status_code=status.HTTP_200_OK,
)
async def read_cells(
        master_id: int,
        date: datetime.date,
        session: AsyncSession = Depends(get_session)
) -> list[CellResponse]:
    return await CellService.get_cells_by_date_and_master_id(
        session=session,
        master_id=master_id,
        search_date=date
    )


@router.get(
    "/free-days/{service_id}",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
)
async def free_day_for_service(
        service_id: int,
        master_id: int,
        session: AsyncSession = Depends(get_session)
) -> list[str]:
    return await CellService.get_days_with_empty_cells_by_service_id_and_master_id(
        service_id=service_id,
        master_id=master_id,
        session=session
    )


@router.get(
    "/free-slots/{service_id}",
    response_model=list[CellResponse],
    status_code=status.HTTP_200_OK,
)
async def free_cells_for_service_in_date(
        date: datetime.date,
        service_id: int,
        master_id: int,
        session: AsyncSession = Depends(get_session)
) -> list[CellResponse]:
    return await CellService.get_ids_with_empty_cells_by_service_id_master_id_in_date(
        record_date=date,
        service_id=service_id,
        master_id=master_id,
        session=session
    )
