from fastapi import APIRouter
from .endpoints.RecordsForUser import router as record_router


router = APIRouter(prefix="/v1")
router.include_router(record_router, tags=["record"])
