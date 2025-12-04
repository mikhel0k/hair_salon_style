from fastapi import APIRouter
from .endpoints.Records import router as record_router


router = APIRouter()
router.include_router(record_router, prefix="/record", tags=["record"])
