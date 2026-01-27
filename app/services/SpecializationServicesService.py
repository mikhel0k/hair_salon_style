from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SpecializationService
from app.schemas.SpecializationService import SpecializationServicesSchema
from app.schemas.Service import ServiceResponse
from app.repositories import SpecializationServiceRepository


async def create_spec_services(
        session: AsyncSession,
        data: SpecializationServicesSchema
):
    try:
        specialization, services, = data.specialization_id, data.services_id
        try:
            spec_services_in_db = set(spec_service.id for spec_service in await
            SpecializationServiceRepository.read_services_by_specialization(
                specialization_id=specialization,
                session=session
            ))
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="SpecializationServices with this data already exists")
        to_add = services - spec_services_in_db
        to_delete = spec_services_in_db - services

        if to_add:
            spec_services_to_add = [SpecializationService(
                specialization_id=specialization,
                service_id=serv
            ) for serv in to_add]
            try:
                await SpecializationServiceRepository.create_specialization_services(
                    session=session,
                    spec_service_data=spec_services_to_add
                )
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="SpecializationServices with this data already exists")
        if to_delete:
            await SpecializationServiceRepository.delete_connection(
                session=session,
                specialization_id=specialization,
                services=to_delete
            )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Something went wrong")

