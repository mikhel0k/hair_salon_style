from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Service
from app.schemas.Service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.repositories import ServiceRepository


async def create_service(
        service: ServiceCreate,
        session: AsyncSession
):
    service_from_db = await ServiceRepository.create_service(
        service=service,
        session=session
    )
    service_data = ServiceResponse.model_validate(service_from_db)
    return service_data


async def get_service_by_id(
        service_id: int,
        session: AsyncSession,
):
    service_from_db = await ServiceRepository.read_service_by_id(
        service_id=service_id,
        session=session
    )
    if not service_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    service_data = ServiceResponse.model_validate(service_from_db)
    return service_data


async def get_services_by_category_id(
        category_id: int,
        session: AsyncSession
):
    services_from_db = await ServiceRepository.read_services_by_category_id(

        category_id=category_id,
        session=session,
    )
    service_data = [ServiceResponse.model_validate(service) for service in services_from_db]
    return service_data


async def update_service(
        service_id: int,
        service: ServiceUpdate,
        session: AsyncSession
):
    service_from_db = await ServiceRepository.read_service_by_id(
        service_id=service_id,
        session=session,
    )
    if not service_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    for key, value in service.model_dump(exclude_unset=True).items():
        setattr(service_from_db, key, value)
    updated_service = await ServiceRepository.update_service(
        service=service_from_db,
        session=session
    )
    service_data = ServiceResponse.model_validate(updated_service)
    return service_data


async def delete_service(
        service_id: int,
        session: AsyncSession
):
    service_from_db = await ServiceRepository.read_service_by_id(
        service_id=service_id,
        session=session
    )
    if not service_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    await ServiceRepository.delete_service(
        service=service_from_db,
        session=session
    )
