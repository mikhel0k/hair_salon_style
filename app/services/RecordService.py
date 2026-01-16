import math

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Cell
from app.schemas.Record import RecordResponse, FullRecordResponse, RecordUpdate, EditRecordStatus, EditRecordNote
from app.schemas.UserFlow import MakeRecord
from app.schemas.User import UserFind, UserCreate
from app.models.Record import Record
from app.repositories import RecordRepository, ServiceRepository, CellRepository, MasterRepository
from app.repositories import UserRepository


async def new_record(
        data: MakeRecord,
        session: AsyncSession,
):
    if not await MasterRepository.checking_master_provides_service(
        master_id=data.master_id,
        session=session,
        service_id=data.service_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Master not provides service"
        )
    user_find = UserFind(phone_number=data.phone_number)
    user = await UserRepository.read_user_by_phone(
        user=user_find,
        session=session
    )
    if not user:
        user_create = UserCreate(
            phone_number=data.phone_number,
        )
        try:
            user = await UserRepository.create_user(
                user=user_create,
                session=session
            )
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Record with this data already exists")
    service = await ServiceRepository.read_service_by_id(
        service_id=data.service_id,
        session=session
    )

    new_cells_id = list(range(data.cell_id, data.cell_id + math.ceil(service.duration_minutes / 15)))
    new_cells = await CellRepository.read_cells(new_cells_id, session)
    for cell in new_cells:
        if cell.status == "free":
            cell.status = "occupied"
        else:
            raise HTTPException(409, f"Cell already occupied")
    await CellRepository.update_cells(new_cells, session)

    record = Record(
        master_id=data.master_id,
        service_id=data.service_id,
        user_id=user.id,
        cell_id=data.cell_id,
        status="created",
        notes=data.notes,
    )
    session.add(record)

    try:
        await session.commit()
        await session.refresh(record)
    except Exception as e:
        await session.rollback()
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении бронирования")

    return RecordResponse.model_validate(record)


async def get_records_hy_phone(
        user: UserFind,
        session: AsyncSession
):
    user_find = await UserRepository.read_user_by_phone(user=user, session=session)
    if not user_find:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    records = await RecordRepository.read_records_by_user_id(
        user_id=user_find.id,
        session=session
    )
    return [FullRecordResponse.model_validate(record) for record in records]


async def update_record(record_id: int, data: RecordUpdate, session: AsyncSession):
    record = await RecordRepository.read_record_by_id(record_id, session)

    new_master_id = data.master_id or record.master_id
    new_service_id = data.service_id or record.service_id
    if not await MasterRepository.checking_master_provides_service(
            master_id=new_master_id,
            session=session,
            service_id=new_service_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Master not provides service"
        )

    if not record:
        raise HTTPException(404, "Record not found")

    old_cell_id = record.cell_id
    new_cell_id = data.cell_id or old_cell_id

    old_service_id = record.service_id
    new_service_id = data.service_id or old_service_id

    service = await ServiceRepository.read_service_by_id(new_service_id, session)

    if new_cell_id != old_cell_id or new_service_id != old_service_id:
        old_cells_id = list(range(old_cell_id,old_cell_id+math.ceil(record.service.duration_minutes / 15)))
        old_cells = await CellRepository.read_cells(old_cells_id, session)
        for cell in old_cells:
            cell.status = "free"
        await CellRepository.update_cells(old_cells, session)


        new_cells_id = list(range(new_cell_id, new_cell_id+math.ceil(service.duration_minutes / 15)))
        new_cells = await CellRepository.read_cells(new_cells_id, session)
        for cell in new_cells:
            if cell.status == "free":
                cell.status = "occupied"
            else:
                raise HTTPException(409, f"Cell already occupied")
        await CellRepository.update_cells(new_cells, session)

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
    try:
        await RecordRepository.update_record(record, session)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "Update failed due to data conflict")

    return RecordResponse.model_validate(record)


async def update_status_record(
        data: EditRecordStatus,
        session: AsyncSession
):
    record = await RecordRepository.read_record_by_id(
        record_id=data.id,
        session=session
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    record.status = data.status
    try:
        await RecordRepository.update_record(
            record=record,
            session=session
        )
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Record with this data already exists"
        )

    return RecordResponse.model_validate(record)


async def update_note_record(
        data: EditRecordNote,
        session: AsyncSession
):
    record = await RecordRepository.read_record_by_id(
        record_id=data.id,
        session=session
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    record.notes = data.notes
    try:
        await RecordRepository.update_record(
            record=record,
            session=session
        )
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Record with this data already exists"
        )
    return RecordResponse.model_validate(record)
