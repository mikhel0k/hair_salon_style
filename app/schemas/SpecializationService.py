from typing import Annotated

from pydantic import BaseModel, Field, StrictInt


ValidateStrictInt = Annotated[StrictInt, Field(ge=1)]

class SpecializationServicesSchema(BaseModel):
    specialization_id: ValidateStrictInt = Field(..., description="ID of the specialization")
    services_id: set[ValidateStrictInt] = Field(..., description="List of service IDs")
