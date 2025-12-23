from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Service import ServiceCreate, ServiceResponse
from app.services.ServiceService import create_service

router = APIRouter()


@router.post("/new_service", response_model=ServiceResponse)
async def new_master(
        master: ServiceCreate,
        session: AsyncSession=Depends(get_session)
):
    return await create_service(session=session, master=master)