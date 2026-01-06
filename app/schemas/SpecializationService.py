from typing import Annotated

from pydantic import BaseModel, Field


class SpecializationServicesSchema(BaseModel):
    specialization_id: Annotated[int, Field(..., ge=1, description="ID of the specialization")]
    services_id: Annotated[set[int], Field(..., ge=1, description="List of service IDs")]
