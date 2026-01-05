from fastapi import APIRouter
from .endpoints.Category import router as category_router
from .endpoints.Service import router as service_router
from .endpoints.Specialization import router as specialization_router
from .endpoints.SpecializationService import router as specialization_service_router
from .endpoints.Master import router as master_router
from .endpoints.Schedule import router as schedule_router


router = APIRouter()
router.include_router(category_router,prefix="/category" ,tags=["category"])
router.include_router(service_router, prefix="/service", tags=["service"])
router.include_router(specialization_router, prefix="/specialization", tags=["specialization"])
router.include_router(specialization_service_router, prefix="/specialization", tags=["specialization"])
router.include_router(master_router, prefix="/master", tags=["master"])
router.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
