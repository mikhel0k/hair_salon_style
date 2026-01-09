from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator, StrictInt

from .validators import name_validator


class SpecializationBase(BaseModel):
    name: Annotated[str, Field(..., max_length=40, min_length=3, description="Name of the specialization")]
    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("name", mode='after')
    @classmethod
    def validate_name(cls, v):
        return name_validator(v)


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationResponse(SpecializationBase):
    id: Annotated[StrictInt, Field(..., ge=1, description="ID of the specialization")]

    model_config = ConfigDict(from_attributes=True)
