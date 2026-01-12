from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.services import SpecializationService
from app.schemas.Specialization import SpecializationCreate, SpecializationResponse


router = APIRouter()


@router.post("/",response_model=SpecializationResponse)
async def create_specialization(
        specialization: SpecializationCreate,
        session: AsyncSession = Depends(get_session),
):
    return await SpecializationService.create_specialization(specialization, session)


@router.get("/{specialization_id}",response_model=SpecializationResponse)
async def get_specialization_by_id(
        specialization_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await SpecializationService.get_specialization_by_id(specialization_id, session)


@router.delete("/{specialization_id}")
async def delete_specialization_by_id(
        specialization_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await SpecializationService.delete_specialization(
        specialization_id=specialization_id,
        session=session
    )
