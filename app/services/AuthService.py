import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, create_token, verify_password
from app.models.Worker import Worker
from app.schemas.Worker import WorkerCreate, Login
from app.repositories import WorkerRepository

logger = logging.getLogger(__name__)


async def registration(
        worker_data: WorkerCreate,
        session: AsyncSession,
):
    logger.debug("registration: username=%s", worker_data.username)
    worker_data.password = get_password_hash(worker_data.password)
    worker = Worker(**worker_data.model_dump())
    try:
        worker_in_db = await WorkerRepository.create_worker(
            session=session,
            worker=worker,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("registration: conflict, username=%s", worker_data.username)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Worker with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("registration: unexpected error, username=%s", worker_data.username)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    data = {
        "sub": str(worker_in_db.id),
        "master_id": worker_in_db.master_id,
        "is_master": worker_in_db.is_master,
        "is_admin": worker_in_db.is_admin,
        "is_active": worker_in_db.is_active,
    }
    try:
        token = create_token(data)
    except Exception as e:
        logger.exception("registration: token creation error, user_id=%s", worker_in_db.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Registration successful: user_id=%s, username=%s", worker_in_db.id, worker_in_db.username)
    return token


def _login_401():
    """Единое сообщение для клиента — не раскрываем причину (безопасность)."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Worker login or password is incorrect",
    )


async def login(
        login_data: Login,
        session: AsyncSession,
):
    logger.debug("Login attempt: username=%s", login_data.username)

    try:
        worker = await WorkerRepository.get_worker_by_username(
            session=session, username=login_data.username
        )
    except Exception as e:
        logger.exception("Login failed: DB error when fetching worker, username=%s", login_data.username)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e

    if not worker:
        logger.info("Login failed: user not found, username=%s", login_data.username)
        raise _login_401()

    if not worker.is_active:
        logger.info(
            "Login failed: user inactive, user_id=%s, username=%s",
            worker.id,
            worker.username,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    try:
        password_ok = verify_password(login_data.password, worker.password)
    except Exception as e:
        logger.exception(
            "Login failed: password verification error, user_id=%s, username=%s",
            worker.id,
            worker.username,
        )
        raise _login_401() from e

    if not password_ok:
        logger.info("Login failed: wrong password, user_id=%s, username=%s", worker.id, worker.username)
        raise _login_401()

    data = {
        "sub": str(worker.id),
        "master_id": worker.master_id,
        "is_master": worker.is_master,
        "is_admin": worker.is_admin,
        "is_active": worker.is_active,
    }
    try:
        token = create_token(data)
    except Exception as e:
        logger.exception(
            "Login failed: token creation error, user_id=%s, username=%s",
            worker.id,
            worker.username,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e

    logger.info(
        "Login successful: user_id=%s, username=%s, is_admin=%s, is_active=%s",
        worker.id,
        worker.username,
        worker.is_admin,
        worker.is_active,
    )
    return token
