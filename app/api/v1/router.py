from fastapi import APIRouter
from .endpoints.Category import router as category_router
from .endpoints.Service import router as service_router
from .endpoints.Specialization import router as specialization_router
from .endpoints.SpecializationService import router as specialization_service_router
from .endpoints.Master import router as master_router
from .endpoints.Schedule import router as schedule_router
from .endpoints.Cell import router as cell_router
from .endpoints.Record import router as record_router
from .endpoints.Auth import router as auth_router
from .endpoints.Feedback import router as feedback_router


router = APIRouter()


router.include_router(category_router,prefix="/category" ,tags=["category"])
router.include_router(service_router, prefix="/service", tags=["service"])
router.include_router(specialization_router, prefix="/specialization", tags=["specialization"])
router.include_router(specialization_service_router, prefix="/specialization", tags=["specialization"])
router.include_router(master_router, prefix="/master", tags=["master"])
router.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
router.include_router(cell_router, prefix="/cell", tags=["cell"])
router.include_router(record_router, prefix="/record", tags=["record"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(feedback_router, prefix="/feedback", tags=["feedback"])
