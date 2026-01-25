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


router = APIRouter()

endpoints = [
    (category_router, "/category/", ["category"]),
    (service_router, "/service/", ["service"]),
    (specialization_router, "/specialization/", ["specialization"]),
    (specialization_service_router, "/specialization/", ["specialization"]),
    (master_router, "/master", ["master"]),
    (schedule_router, "/schedule", ["schedule"]),
    (cell_router, "/cell", ["cell"]),
    (record_router, "/record", ["record"]),
    (auth_router, "/auth", ["auth"]),
]

for endpoint, prefix, tags in endpoints:
    router.include_router(endpoint, prefix=prefix, tags=tags)
