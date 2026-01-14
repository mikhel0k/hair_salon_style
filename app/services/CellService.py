from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta, datetime
import math

from app.repositories import ScheduleRepository, CellRepository, ServiceRepository
from app.schemas.Cell import CellCreate
from app.schemas.Schedule import ScheduleResponse

DAYS_IN_WEEK = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

async def make_cells(
        master_id,
        session: AsyncSession,
):
    schedule_in_db = await ScheduleRepository.read_schedule_by_master_id(master_id=master_id, session=session)
    if not schedule_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    schedule = ScheduleResponse.model_validate(schedule_in_db)
    cells = []
    today = date.today()
    current_date = today - timedelta(days=today.weekday())
    for day in DAYS_IN_WEEK:
        if current_date < today:
            current_date += timedelta(days=1)
            continue
        start, end = f"{day}_start", f"{day}_end"
        start_time, end_time = getattr(schedule, start), getattr(schedule, end)
        if start_time is None or end_time is None:
            current_date += timedelta(days=1)
            continue
        start_time = datetime.combine(current_date, start_time)
        end_time = datetime.combine(current_date, end_time)
        while start_time <= end_time:
            cells.append(
                CellCreate(
                    master_id=master_id,
                    date=current_date,
                    time=start_time.time(),
                    status="free"
                )
            )
            start_time += timedelta(minutes=15)
        current_date += timedelta(days=1)
    try:
        await session.rollback()
        await CellRepository.create_cells(sells_list=cells, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cell with this data already exists")


async def get_cells_by_date_and_master_id(
        master_id: int,
        search_date: date,
        session: AsyncSession
):
    return await CellRepository.read_cells_by_master_id_and_date(
        master_id = master_id,
        cell_date = search_date,
        session = session
    )


async def get_free_cells_by_service_id_and_master_id(
        service_id: int,
        master_id: int,
        session: AsyncSession
):
    cells = await CellRepository.read_cells_by_master_id(
        master_id = master_id,
        session = session
    )
    if not cells:
        return {
            "message" : "No free cells found",
        }
    service = await ServiceRepository.read_service_by_id(service_id=service_id, session=session)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    required_slots = math.ceil(service.duration_minutes/15)
    response=[]
    l, r = 0, required_slots
    for i in range(len(cells) - required_slots + 1):
        window = cells[i: i + required_slots]

        is_free = all(c.status == "free" for c in window)
        same_day = all(c.date == window[0].date for c in window)

        if is_free and same_day:
            response.append(window[0])

    return response
