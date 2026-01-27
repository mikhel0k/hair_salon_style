from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_session
from app.core.dependencies import is_user_admin
from app.schemas.Service import ServiceResponse
from app.schemas.SpecializationService import SpecializationServicesSchema
from app.services import SpecializationServicesService


router = APIRouter()


@router.put(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_specialization_service(
        specialization_service: SpecializationServicesSchema,
        admin_user = Depends(is_user_admin),
        session: AsyncSession = Depends(get_session)
):
    await SpecializationServicesService.create_spec_services(
        data=specialization_service,
        session=session
    )
    return {"status": "success"}
