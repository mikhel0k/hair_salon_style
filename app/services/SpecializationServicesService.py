from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SpecializationService, Service
from app.schemas.SpecializationService import SpecializationServicesSchema
from app.schemas.Service import ServiceResponse
from app.repositories import SpecializationServiceRepository


async def create_spec_services(
        session: AsyncSession,
        data: SpecializationServicesSchema
):
    specialization, services, = data.specialization_id, data.services_id
    spec_services_in_db = set(spec_service.service_id for spec_service in await
    SpecializationServiceRepository.read_services_by_specialization(
        specialization_id=specialization,
        session=session
    ))
    to_add = services - spec_services_in_db
    to_delete = spec_services_in_db - services

    if to_add:
        spec_services_to_add = [SpecializationService(
            specialization_id=specialization,
            service_id=serv
        ) for serv in to_add]
        await SpecializationServiceRepository.create_specialization_services(
            session=session,
            spec_service_data=spec_services_to_add
        )
    if to_delete:
        await SpecializationServiceRepository.delete_connection(
            session=session,
            specialization_id=specialization,
            services=to_delete
        )
    await session.commit()


async def read_services_by_specialization_id(
        specialization_id: int,
        session: AsyncSession
):
    services = await SpecializationServiceRepository.read_services_by_specialization(
        specialization_id=specialization_id,
        session=session
    )
    return [ServiceResponse.model_validate(service) for service in services]
