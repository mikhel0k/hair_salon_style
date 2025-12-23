from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ServiceRepository
from app.schemas.Service import ServiceCreate, ServiceResponse, ServiceUpdate
import app.repositories.MasterRepository


async def create_service(service: ServiceCreate, session: AsyncSession) -> ServiceResponse:
    service_record = await ServiceRepository.create_service(service, session)
    return ServiceResponse.model_validate(service_record)


async def get_services(session: AsyncSession, skip: int, limit: int) -> list[ServiceResponse] | None:
    services = await ServiceRepository.get_services(session, skip, limit)
    return [ServiceResponse.model_validate(service) for service in services]

async def get_services_by_category(session: AsyncSession, skip: int, limit: int, category) -> list[ServiceResponse] | None:
    services = await ServiceRepository.get_services_by_category(
        session=session,
        category=category,
        limit=limit,
        skip=skip
    )
    return [ServiceResponse.model_validate(service) for service in services]

async def update_service_by_id(service_id: int, service: ServiceUpdate, session: AsyncSession) -> ServiceResponse:
    service = await ServiceRepository.update_service_by_id(
        service_id=service_id,
        service=service,
        session=session
    )
    return ServiceResponse.model_validate(service)

async def delete_service_by_id(service_id: int, session: AsyncSession):
    await ServiceRepository.delete_service_by_id(
        service_id=service_id,
        session=session
    )
