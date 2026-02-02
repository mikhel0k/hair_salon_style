import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

from app.schemas.Specialization import SpecializationCreate, SpecializationResponse
from app.repositories import (
    SpecializationRepository,
    SpecializationServiceRepository,
    MasterRepository,
)
from app.schemas.SpecializationService import SpecializationWithServicesResponse


async def create_specialization(
        specialization: SpecializationCreate,
        session: AsyncSession,
):
    logger.debug("create_specialization: name=%s", specialization.name)
    try:
        specialization_in_db = await SpecializationRepository.create_specialization(
            specialization_data=specialization,
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("create_specialization: conflict, name=%s", specialization.name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Specialization with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("create_specialization: unexpected error, name=%s", specialization.name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Specialization created: id=%s, name=%s", specialization_in_db.id, specialization_in_db.name)
    return SpecializationResponse.model_validate(specialization_in_db)


async def get_specialization_by_id(
        specialization_id: int,
        session: AsyncSession,
):
    specialization_in_db = await SpecializationRepository.read_specialization(
        specialization_id=specialization_id,
        session=session,
    )
    if not specialization_in_db:
        logger.info("get_specialization_by_id: not found, specialization_id=%s", specialization_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialization not found",
        )
    return SpecializationWithServicesResponse.model_validate(specialization_in_db)


async def get_specializations(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    specializations = await SpecializationRepository.read_specializations(
        skip=skip,
        limit=limit,
        session=session
    )
    return [SpecializationResponse.model_validate(specialization) for specialization in specializations]


async def delete_specialization(
        specialization_id: int,
        session: AsyncSession,
):
    logger.debug("delete_specialization: specialization_id=%s", specialization_id)
    specialization_from_db = await SpecializationRepository.read_specialization(
        specialization_id=specialization_id,
        session=session,
    )
    if not specialization_from_db:
        logger.info("delete_specialization: not found, specialization_id=%s", specialization_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialization not found",
        )
    masters_count = await MasterRepository.count_masters_by_specialization_id(
        specialization_id=specialization_id,
        session=session,
    )
    if masters_count > 0:
        logger.info(
            "delete_specialization: specialization has linked masters, specialization_id=%s",
            specialization_id,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete specialization: it has linked masters. Remove or reassign masters first.",
        )
    try:
        await SpecializationServiceRepository.delete_all_by_specialization_id(
            specialization_id=specialization_id,
            session=session,
        )
        await SpecializationRepository.delete_specialization(
            specialization=specialization_from_db,
            session=session,
        )
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.exception(
            "delete_specialization: unexpected error, specialization_id=%s",
            specialization_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info(
        "Specialization deleted: id=%s, name=%s",
        specialization_from_db.id,
        specialization_from_db.name,
    )
