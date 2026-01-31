import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SpecializationService
from app.schemas.SpecializationService import SpecializationServicesSchema
from app.repositories import SpecializationServiceRepository, SpecializationRepository

logger = logging.getLogger(__name__)


async def create_spec_services(
        session: AsyncSession,
        data: SpecializationServicesSchema
):
    specialization_id, services_id = data.specialization_id, data.services_id
    logger.debug(
        "create_spec_services: specialization_id=%s, services_count=%s",
        specialization_id,
        len(services_id),
    )

    specialization = await SpecializationRepository.read_specialization(
        specialization_id=specialization_id,
        session=session,
    )
    if not specialization:
        logger.info("create_spec_services: specialization not found, id=%s", specialization_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialization not found",
        )

    try:
        spec_services_in_db = set(
            s.id for s in await SpecializationServiceRepository.read_services_by_specialization(
                specialization_id=specialization_id,
                session=session,
            )
        )
    except Exception as e:
        logger.exception(
            "create_spec_services: error reading services, specialization_id=%s",
            specialization_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e

    to_add = services_id - spec_services_in_db
    to_delete = spec_services_in_db - services_id

    if to_add:
        spec_services_to_add = [
            SpecializationService(specialization_id=specialization_id, service_id=serv)
            for serv in to_add
        ]
        try:
            await SpecializationServiceRepository.create_specialization_services(
                session=session,
                spec_service_data=spec_services_to_add,
            )
        except IntegrityError:
            await session.rollback()
            logger.info("create_spec_services: conflict on create, specialization_id=%s", specialization_id)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="SpecializationServices with this data already exists",
            )
    if to_delete:
        await SpecializationServiceRepository.delete_connection(
            session=session,
            specialization_id=specialization_id,
            services=to_delete,
        )
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("create_spec_services: conflict on commit, specialization_id=%s", specialization_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Something went wrong",
        )
    except Exception as e:
        await session.rollback()
        logger.exception(
            "create_spec_services: unexpected error, specialization_id=%s",
            specialization_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info(
        "SpecializationServices updated: specialization_id=%s, added=%s, deleted=%s",
        specialization_id,
        len(to_add),
        len(to_delete),
    )

