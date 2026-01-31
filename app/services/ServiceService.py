import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.repositories import ServiceRepository

logger = logging.getLogger(__name__)


async def create_service(
        service: ServiceCreate,
        session: AsyncSession
):
    logger.debug("create_service: name=%s, category_id=%s", service.name, service.category_id)
    try:
        service_from_db = await ServiceRepository.create_service(
            service=service,
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("create_service: conflict, name=%s", service.name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("create_service: unexpected error, name=%s", service.name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Service created: id=%s, name=%s", service_from_db.id, service_from_db.name)
    return ServiceResponse.model_validate(service_from_db)


async def get_services(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    service_from_db = await ServiceRepository.read_services(
        skip = skip,
        limit = limit,
        session=session
    )
    return [ServiceResponse.model_validate(service) for service in service_from_db]


async def get_services_by_category_id(
        category_id: int,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    services_from_db = await ServiceRepository.read_services_by_category_id(
        category_id=category_id,
        session=session,
        skip=skip,
        limit=limit
    )
    service_data = [ServiceResponse.model_validate(service) for service in services_from_db]
    return service_data


async def update_service(
        service_id: int,
        service: ServiceUpdate,
        session: AsyncSession
):
    logger.debug("update_service: service_id=%s", service_id)
    service_from_db = await ServiceRepository.read_service_by_id(
        service_id=service_id,
        session=session,
    )
    if not service_from_db:
        logger.info("update_service: not found, service_id=%s", service_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    for key, value in service.model_dump(exclude_unset=True).items():
        setattr(service_from_db, key, value)
    try:
        updated_service = await ServiceRepository.update_service(
            service=service_from_db,
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("update_service: conflict, service_id=%s", service_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("update_service: unexpected error, service_id=%s", service_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Service updated: id=%s, name=%s", updated_service.id, updated_service.name)
    return ServiceResponse.model_validate(updated_service)


async def delete_service(
        service_id: int,
        session: AsyncSession
):
    logger.debug("delete_service: service_id=%s", service_id)
    service_from_db = await ServiceRepository.read_service_by_id(
        service_id=service_id,
        session=session,
    )
    if not service_from_db:
        logger.info("delete_service: not found, service_id=%s", service_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    try:
        await ServiceRepository.delete_service(
            service=service_from_db,
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("delete_service: conflict, service_id=%s", service_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("delete_service: unexpected error, service_id=%s", service_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Service deleted: id=%s, name=%s", service_from_db.id, service_from_db.name)
