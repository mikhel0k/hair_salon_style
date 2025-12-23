from fastapi import APIRouter
from .endpoints.Records import router as record_router
from .endpoints.Master import router as master_router


router = APIRouter()
router.include_router(record_router, prefix="/record", tags=["record"])
router.include_router(master_router, prefix="/master", tags=["master"])
