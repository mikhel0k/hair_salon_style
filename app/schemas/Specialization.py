from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class SpecializationBase(BaseModel):
    name: Annotated[str, Field(..., max_length=40, min_length=3, description="Name of the specialization")]
    model_config = ConfigDict(str_strip_whitespace=True)


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationResponse(SpecializationBase):
    id: Annotated[int, Field(..., ge=1, description="ID of the specialization")]

    model_config = ConfigDict(from_attributes=True)
