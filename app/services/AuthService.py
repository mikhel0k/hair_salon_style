from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, create_token
from app.models.Worker import Worker
from app.schemas.Worker import WorkerCreate
from app.repositories import WorkerRepository


async def registration(
        worker_data: WorkerCreate,
        session: AsyncSession,
):
    worker_data.password = get_password_hash(worker_data.password)
    worker = Worker(**worker_data.model_dump())
    try:
        worker_in_db = await WorkerRepository.create_worker(
            session=session,
            worker=worker,
        )
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Worker with this data already exists")
    data = {
        "sub": worker_in_db.id,
        "is_master": worker_in_db.is_master,
        "is_admin": worker_in_db.is_admin,
        "is_active": worker_in_db.is_active,
    }
    token = create_token(data)
    return token
