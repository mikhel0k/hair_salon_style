from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import MasterRepository
from app.schemas.Master import MasterCreate, MasterResponse
import app.repositories.MasterRepository


async def create_master(master: MasterCreate, session: AsyncSession) -> MasterResponse:
    master_record = await MasterRepository.create_master(master, session)
    return MasterResponse.model_validate(master_record)
