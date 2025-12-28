from fastapi import APIRouter
from .endpoints.Category import router as category_router
from .endpoints.Service import router as service_router


router = APIRouter()
router.include_router(category_router,prefix="/category" ,tags=["category"])
router.include_router(service_router, prefix="/service", tags=["service"])
