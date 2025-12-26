from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class SpecializationBase(BaseModel):
    name: Annotated[str, Field(..., description="Name of the specialization")]


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationResponse(SpecializationBase):
    id: Annotated[int, Field(..., description="ID of the specialization")]

    model_config = ConfigDict(from_attributes=True)
