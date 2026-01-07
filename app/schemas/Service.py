import decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

from .validators import name_validator


class ServiceBase(BaseModel):
    name: Annotated[str, Field(..., max_length=60, min_length=3, description="Name of the service")]
    price: Annotated[decimal.Decimal, Field(..., ge=1, le=10000, description="Price of the service")]
    duration_minutes: Annotated[int, Field(..., ge=10, le=180, description="Duration of the service")]
    category_id: Annotated[int, Field(..., ge=1, description="Category of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v):
        return name_validator(v)


    model_config = ConfigDict(str_strip_whitespace=True)


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: Annotated[int, Field(..., ge=1, description="ID of the service")]

    model_config = ConfigDict(from_attributes=True)


class ServiceResponseSmall(BaseModel):
    id: Annotated[int, Field(..., ge=1, description="ID of the service")]
    name: Annotated[str, Field(..., max_length=60, min_length=3,  description="Name of the service")]
    price: Annotated[decimal.Decimal, Field(..., ge=1, le=10000, description="Price of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v):
        return name_validator(v)

    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)


class ServiceUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, max_length=60, min_length=3, description="Name of the service")]
    price: Annotated[Optional[decimal.Decimal], Field(None, ge=1, le=10000, description="Price of the service")]
    duration_minutes: Annotated[Optional[int], Field(None, ge=10, le=180, description="Duration of the service")]
    category_id: Annotated[Optional[int], Field(None, ge=1, description="Category of the service")]
    description: Annotated[Optional[str], Field(None, description="Description of the service")]


    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v):
        return name_validator(v)

    model_config = ConfigDict(str_strip_whitespace=True)
