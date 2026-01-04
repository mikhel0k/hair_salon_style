from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.SpecializationService import SpecializationServicesSchema
from app.services import SpecializationServicesService


router = APIRouter()


@router.post("/update")
async def update_specialization_service(
        specialization_service: SpecializationServicesSchema,
        session: AsyncSession = Depends(get_session)
):
    await SpecializationServicesService.create_spec_services(
        data=specialization_service,
        session=session
    )