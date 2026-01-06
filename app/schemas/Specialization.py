from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator

from .validators import name_validator


class SpecializationBase(BaseModel):
    name: Annotated[str, Field(..., max_length=40, min_length=3, description="Name of the specialization")]
    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("name", mode='before')
    @classmethod
    def name_validator(cls, v):
        return name_validator(v)


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationResponse(SpecializationBase):
    id: Annotated[int, Field(..., ge=1, description="ID of the specialization")]

    model_config = ConfigDict(from_attributes=True)
