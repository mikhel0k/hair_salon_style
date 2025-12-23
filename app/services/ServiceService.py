from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ServiceRepository
from app.schemas.Service import ServiceCreate, ServiceResponse
import app.repositories.MasterRepository


async def create_service(master: ServiceCreate, session: AsyncSession) -> ServiceResponse:
    master_record = await ServiceRepository.create_service(master, session)
    return ServiceResponse.model_validate(master_record)
