from typing import Annotated

from pydantic import BaseModel, Field, StrictInt


class SpecializationServicesSchema(BaseModel):
    specialization_id: Annotated[StrictInt, Field(..., ge=1, description="ID of the specialization")]
    services_id: Annotated[set[StrictInt], Field(..., ge=1, description="List of service IDs")]
