from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_session
from app.core.dependencies import is_user_admin
from app.services import SpecializationService
from app.schemas.Specialization import SpecializationCreate, SpecializationResponse


router = APIRouter()


@router.post(
    "/",
    response_model=SpecializationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_specialization(
        specialization_data: SpecializationCreate,
        admin_user = Depends(is_user_admin),
        session: AsyncSession = Depends(get_session),
):
    return await SpecializationService.create_specialization(
        specialization=specialization_data,
        session=session,
    )


@router.get(
    "/{specialization_id}",
    response_model=SpecializationResponse,
    status_code=status.HTTP_200_OK,
)
async def get_specialization_by_id(
        specialization_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await SpecializationService.get_specialization_by_id(
        specialization_id=specialization_id,
        session=session,
    )


@router.delete(
    "/{specialization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_specialization_by_id(
        specialization_id: int,
        admin_user = Depends(is_user_admin),
        session: AsyncSession = Depends(get_session),
):
    await SpecializationService.delete_specialization(
        specialization_id=specialization_id,
        session=session
    )
