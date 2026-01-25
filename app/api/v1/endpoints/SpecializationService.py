from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_session
from app.schemas.SpecializationService import SpecializationServicesSchema
from app.services import SpecializationServicesService


router = APIRouter()


@router.put(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_specialization_service(
        specialization_service: SpecializationServicesSchema,
        session: AsyncSession = Depends(get_session)
):
    await SpecializationServicesService.create_spec_services(
        data=specialization_service,
        session=session
    )
    return {"status": "success"}


@router.get(
    "/{specialization_id}",
    response_model=list[SpecializationServicesSchema],
    status_code=status.HTTP_200_OK,
)
async def get_specialization_services(
        specialization_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await SpecializationServicesService.read_services_by_specialization_id(
        specialization_id=specialization_id,
        session=session
    )
