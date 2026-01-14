from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Service import ServiceResponse, ServiceCreate, ServiceUpdate
from app.core import get_session
from app.services import ServiceService


router = APIRouter()


@router.post("/",response_model=ServiceResponse)
async def create_service(
        service: ServiceCreate,
        session: AsyncSession = Depends(get_session)
):
    return await ServiceService.create_service(
        service=service,
        session=session
    )



# @router.get("/by_id/{service_id}",response_model=ServiceResponse)
# async def get_service_by_id(
#         service_id: int,
#         session: AsyncSession = Depends(get_session)
# ):
#     return await ServiceService.get_service_by_id(
#         service_id=service_id,
#         session=session
#     )


@router.get("/{category_id}", )
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


@router.patch("/{service_id}")
async def update_service(
        service_id: int,
        service: ServiceUpdate,
        session: AsyncSession = Depends(get_session)
):
    return await ServiceService.update_service(
        service_id=service_id,
        service=service,
        session=session
    )


@router.delete("/{service_id}")
async def delete_service(
        service_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await ServiceService.delete_service(
        service_id=service_id,
        session=session
    )
