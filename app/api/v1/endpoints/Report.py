from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_session
from app.core.dependencies import is_user_admin
from app.core.validators import parse_report_date
from app.schemas.Report import MasterReportResponse
from app.services import ReportService

router = APIRouter()


@router.get(
    "/",
    response_model=MasterReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Выгрузка по мастеру за период",
    description="Доступно только администратору. Возвращает отчёт по записям выбранного мастера с date_from по date_to (включительно). Форматы даты: YYYY-MM-DD, YYYY.MM.DD, DD-MM-YYYY, DD.MM.YYYY.",
)
async def get_master_report(
        master_id: int = Query(..., ge=1, description="ID мастера"),
        date_from: str = Query(..., description="Начало периода (YYYY-MM-DD, YYYY.MM.DD, DD-MM-YYYY или DD.MM.YYYY)"),
        date_to: str = Query(..., description="Конец периода (YYYY-MM-DD, YYYY.MM.DD, DD-MM-YYYY или DD.MM.YYYY)"),
        admin_user=Depends(is_user_admin),
        session: AsyncSession = Depends(get_session),
):
    try:
        from_date = parse_report_date(date_from)
        to_date = parse_report_date(date_to)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e.args[0]) if e.args else "Invalid date format",
        )
    return await ReportService.get_master_report(
        master_id=master_id,
        date_from=from_date,
        date_to=to_date,
        session=session,
    )
