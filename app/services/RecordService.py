from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Record import RecordResponse, FullRecordResponse, RecordUpdate, EditRecordStatus, EditRecordNote
from app.schemas.UserFlow import MakeRecord
from app.schemas.User import UserFind, UserCreate
from app.models.Record import Record
from app.repositories import RecordRepository, ServiceRepository, CellRepository
from app.repositories import UserRepository


async def new_record(
        data: MakeRecord,
        session: AsyncSession,
):
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
    record = Record(
        master_id=data.master_id,
        service_id=data.service_id,
        user_id=user.id,
        cell_id=data.cell_id,
        status="created",
        notes=data.notes,
    )
    try:
        record = await RecordRepository.create_record(
            record=record,
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
    need_cells_counter = service.duration_minutes/15
    cells, cell_id = [], data.cell_id
    for i in range(int(need_cells_counter)):
        cell = await CellRepository.read_cell(
            cell_id=cell_id,
            session=session
        )
        cell.status = "occupied"
        cells.append(cell)
        cell_id += 1

    try:
        await CellRepository.update_cells(
            cells=cells,
            session=session
        )
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Record with this data already exists")

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


async def update_record(
        record_id: int,
        data: RecordUpdate,
        session: AsyncSession
):
    record = await RecordRepository.read_record_by_id(
        record_id=record_id,
        session=session
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
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
