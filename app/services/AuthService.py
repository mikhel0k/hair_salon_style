from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, create_token, verify_password
from app.models.Worker import Worker
from app.schemas.Worker import WorkerCreate, Login
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
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Worker with this data already exists")
    data = {
        "sub": str(worker_in_db.id),
        "master_id": worker_in_db.master_id,
        "is_master": worker_in_db.is_master,
        "is_admin": worker_in_db.is_admin,
        "is_active": worker_in_db.is_active,
    }
    token = create_token(data)
    return token


async def login(
        login_data: Login,
        session: AsyncSession,
):
    worker = await WorkerRepository.get_worker_by_username(session=session, username=login_data.username)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Worker login or password is incorrect"
        )
    if verify_password(login_data.password, worker.password):
        data = {
            "sub": str(worker.id),
            "master_id": worker.master_id,
            "is_master": worker.is_master,
            "is_admin": worker.is_admin,
            "is_active": worker.is_active,
        }
        token = create_token(data)
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Worker login or password is incorrect"
        )
