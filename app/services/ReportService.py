import logging
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import MasterRepository, RecordRepository
from app.schemas.Report import MasterReportResponse, MasterReportRow

logger = logging.getLogger(__name__)


async def get_master_report(
        master_id: int,
        date_from: date,
        date_to: date,
        session: AsyncSession,
) -> MasterReportResponse:
    """
    Формирует выгрузку по мастеру за период (только для админа).
    date_from и date_to включаются в период.
    """
    if date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="date_from must be less than or equal to date_to",
        )

    master = await MasterRepository.read_master(master_id=master_id, session=session)
    if not master:
        logger.info("get_master_report: master not found, master_id=%s", master_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found",
        )

    records = await RecordRepository.read_records_by_master_id_and_time_interval_for_report(
        master_id=master_id,
        date_start=date_from,
        date_end=date_to,
        session=session,
    )

    rows = [
        MasterReportRow(
            record_id=rec.id,
            date=rec.cell.date,
            time=rec.cell.time,
            service_name=rec.service.name,
            service_price=rec.service.price,
            status=rec.status.value if hasattr(rec.status, "value") else str(rec.status),
            client_phone=rec.user.phone_number,
            notes=rec.notes,
        )
        for rec in records
    ]

    logger.info(
        "Report generated: master_id=%s, date_from=%s, date_to=%s, total=%s",
        master_id, date_from, date_to, len(rows),
    )
    return MasterReportResponse(
        master_id=master.id,
        master_name=master.name,
        date_from=date_from,
        date_to=date_to,
        total_records=len(rows),
        records=rows,
    )
