from typing import Annotated

from pydantic import BaseModel, Field, StrictInt, ConfigDict

from app.schemas.Service import ServiceResponse

ValidateStrictInt = Annotated[StrictInt, Field(ge=1)]

class SpecializationServicesSchema(BaseModel):
    specialization_id: ValidateStrictInt = Field(..., description="ID of the specialization")
    services_id: set[ValidateStrictInt] = Field(..., description="List of service IDs")


class SpecializationWithServicesResponse(BaseModel):
    id: int
    name: str
    services: list['ServiceResponse'] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
