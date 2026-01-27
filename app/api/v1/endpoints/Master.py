from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.core.dependencies import is_user_admin
from app.schemas.Master import MasterResponse, MasterCreate, MasterUpdate, MasterFullResponse
from app.services import MasterService


router = APIRouter()


@router.post(
    "/",
    response_model=MasterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_master(
        master_data: MasterCreate,
        admin_user = Depends(is_user_admin),
        session: AsyncSession=Depends(get_session)
):
    return await MasterService.create_master(
        master=master_data,
        session=session,
    )


@router.get(
    "/",
    response_model=list[MasterFullResponse],
    status_code=status.HTTP_200_OK,
)
async def get_masters(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_session)
):
    return await MasterService.get_masters(
        skip=skip,
        limit=limit,
        session=session,
    )


@router.get(
    "/by-service/{service_id}",
    response_model=list[MasterResponse],
    status_code=status.HTTP_200_OK,
)
async def get_masters_by_service_id(
        service_id: int,
        session: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100,
):
    return await MasterService.get_masters_by_service_id(
        service_id=service_id,
        session=session,
        skip=skip,
        limit=limit
    )


@router.patch(
    "/{master_id}",
    response_model=MasterResponse,
    status_code=status.HTTP_200_OK,
)
async def update_master(
        master_id: int,
        master_data: MasterUpdate,
        admin_user = Depends(is_user_admin),
        session: AsyncSession = Depends(get_session),
):
    return await MasterService.update_master(
        master_id=master_id,
        master_data=master_data,
        session=session,
    )
