from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.dependencies import is_user_admin
from app.schemas.Service import ServiceResponse, ServiceCreate, ServiceUpdate
from app.core import get_session
from app.services import ServiceService


router = APIRouter()


@router.post(
    "/",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
        service_data: ServiceCreate,
        admin_user = Depends(is_user_admin),
        session: AsyncSession = Depends(get_session)
):
    return await ServiceService.create_service(
        service=service_data,
        session=session
    )


@router.get(
    "/",
    response_model=list[ServiceResponse],
    status_code=status.HTTP_200_OK,
)
async def get_services(
        session: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100
):
    return await ServiceService.get_services(
        session=session,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{category_id}",
    response_model=list[ServiceResponse],
    status_code=status.HTTP_200_OK,
)
async def get_services_by_category(
        category_id: int,
        session: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100
):
    return await ServiceService.get_services_by_category_id(
        category_id=category_id,
        session=session,
        skip=skip,
        limit=limit
    )


@router.patch(
    "/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_service(
        service_id: int,
        service: ServiceUpdate,
        admin_user = Depends(is_user_admin),
        session: AsyncSession = Depends(get_session)
):
    return await ServiceService.update_service(
        service_id=service_id,
        service=service,
        session=session
    )


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
        service_id: int,
        admin_user = Depends(is_user_admin),
        session: AsyncSession = Depends(get_session)
):
    await ServiceService.delete_service(
        service_id=service_id,
        session=session
    )
