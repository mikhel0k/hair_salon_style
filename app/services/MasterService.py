import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Master
from app.schemas.Master import MasterCreate, MasterUpdate, MasterResponse, MasterFullResponse
from app.repositories import MasterRepository, ScheduleRepository
from app.schemas.Schedule import ScheduleCreate

logger = logging.getLogger(__name__)


async def create_master(
        master: MasterCreate,
        session: AsyncSession
):
    logger.debug("create_master: name=%s", master.name)
    master_obj = Master(**master.model_dump())
    try:
        master_in_db = await MasterRepository.create_master(master=master_obj, session=session)
        await ScheduleRepository.create_schedule(
            ScheduleCreate(id=master_in_db.id, master_id=master_in_db.id),
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("create_master: conflict, name=%s", master.name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Master with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("create_master: unexpected error, name=%s", master.name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Master created: id=%s, name=%s", master_in_db.id, master_in_db.name)
    return MasterResponse.model_validate(master_in_db)


async def update_master(
        master_id: int,
        master_data: MasterUpdate,
        session: AsyncSession
):
    logger.debug("update_master: master_id=%s", master_id)
    master = await MasterRepository.read_master(master_id=master_id, session=session)
    if master is None:
        logger.info("update_master: not found, master_id=%s", master_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found",
        )
    for key, value in master_data.model_dump(exclude_unset=True).items():
        setattr(master, key, value)
    try:
        master_in_db = await MasterRepository.update_master(master=master, session=session)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("update_master: conflict, master_id=%s", master_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Master with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("update_master: unexpected error, master_id=%s", master_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Master updated: id=%s, name=%s", master_in_db.id, master_in_db.name)
    return MasterResponse.model_validate(master_in_db)


async def get_masters(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    masters = await MasterRepository.read_masters(skip=skip, limit=limit, session=session)
    return [MasterFullResponse.model_validate(master) for master in masters]


async def get_masters_by_service_id(
        service_id: int,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
):
    masters = await MasterRepository.read_masters_by_service_id(
        service_id=service_id,
        session=session,
        skip=skip,
        limit=limit,
    )
    return [MasterResponse.model_validate(master) for master in masters]
