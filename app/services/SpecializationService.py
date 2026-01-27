from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Specialization import SpecializationCreate, SpecializationResponse
from app.repositories import SpecializationRepository
from app.schemas.SpecializationService import SpecializationWithServicesResponse


async def create_specialization(
        specialization: SpecializationCreate,
        session: AsyncSession,
):
    try:
        specialization_in_db = await SpecializationRepository.create_specialization(
            specialization_data=specialization,
            session=session
        )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Specialization with this data already exists")
    specialization_data = SpecializationResponse.model_validate(specialization_in_db)
    return specialization_data


async def get_specialization_by_id(
        specialization_id: int,
        session: AsyncSession,
):
    specialization_in_db = await SpecializationRepository.read_specialization(
        specialization_id=specialization_id,
        session=session
    )
    if not specialization_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specialization not found")
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
