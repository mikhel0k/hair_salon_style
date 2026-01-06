from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Record import RecordResponse
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
        user = await UserRepository.create_user(
            user=user_create,
            session=session
        )
    record = Record(
        master_id=data.master_id,
        service_id=data.service_id,
        user_id=user.id,
        cell_id=data.cell_id,
        status="created",
        notes=data.notes,
    )
    record = await RecordRepository.create_record(
        record=record,
        session=session
    )
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

    await CellRepository.update_cells(
        cells=cells,
        session=session
    )

    return RecordResponse.model_validate(record)
