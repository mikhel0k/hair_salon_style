from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Service import ServiceCreate, ServiceResponse, ServiceUpdate
from app.services.ServiceService import (
    create_service,
    get_services,
    get_services_by_category,
    update_service_by_id,
    delete_service_by_id
)

router = APIRouter()


@router.post("/new_service", response_model=ServiceResponse)
async def new_master(
        service: ServiceCreate,
        session: AsyncSession=Depends(get_session)
):
    return await create_service(session=session, service=service)

@router.get("/services", response_model=List[ServiceResponse] | None)
async def get_services_paginated(
        session: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100
):
    return await get_services(session, skip, limit)

@router.get("/services/{category}", response_model=List[ServiceResponse] | None)
async def get_services_by_category_paginated(
        category: str,
        session: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100
):
    return await get_services_by_category(session, skip, limit, category)

@router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
        service_id: int,
        service: ServiceUpdate,
        session: AsyncSession = Depends(get_session)
):
    return await update_service_by_id(
        service=service,
        service_id=service_id,
        session=session
    )

@router.delete("/{service_id}", status_code=204)
async def delete_service(
        service_id: int,
        session: AsyncSession = Depends(get_session)
):
    await delete_service_by_id(
        service_id=service_id,
        session=session
    )
