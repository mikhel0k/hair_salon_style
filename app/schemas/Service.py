import decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class ServiceBase(BaseModel):
    name: Annotated[str, Field(..., max_length=60, min_length=3, description="Name of the service")]
    price: Annotated[decimal.Decimal, Field(..., description="Price of the service")]
    duration_minutes: Annotated[int, Field(..., description="Duration of the service")]
    category_id: Annotated[int, Field(..., ge=1, description="Category of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]

    @field_validator("duration_minutes")
    @classmethod
    def validate_duration_minutes(cls, v):
        if v <= 0:
            raise ValueError("Duration must be greater than 0")
        elif v > 180:
            raise ValueError("Duration must be less than 3 hours")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        elif v > 10000:
            raise ValueError("Price must be less than 10000")
        return v

    model_config = ConfigDict(str_strip_whitespace=True)


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: Annotated[int, Field(..., ge=1, description="ID of the service")]

    model_config = ConfigDict(from_attributes=True)


class ServiceResponseSmall(BaseModel):
    id: Annotated[int, Field(..., description="ID of the service")]
    name: Annotated[str, Field(..., max_length=60, min_length=3,  description="Name of the service")]
    price: Annotated[decimal.Decimal, Field(..., description="Price of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]


    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        elif v > 10000:
            raise ValueError("Price must be less than 10000")
        return v

    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)


class ServiceUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, max_length=60, min_length=3, description="Name of the service")]
    price: Annotated[Optional[decimal.Decimal], Field(None, description="Price of the service")]
    duration_minutes: Annotated[Optional[int], Field(None, description="Duration of the service")]
    category_id: Annotated[Optional[int], Field(None, ge=1, description="Category of the service")]
    description: Annotated[Optional[str], Field(None, description="Description of the service")]

    @field_validator("duration_minutes")
    @classmethod
    def validate_duration_minutes(cls, v):
        if v is None:
            return v
        elif v <= 0:
            raise ValueError("Duration must be greater than 0")
        elif v > 180:
            raise ValueError("Duration must be less than 3 hours")
        return v


    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is None:
            return v
        elif v <= 0:
            raise ValueError("Price must be greater than 0")
        elif v > 10000:
            raise ValueError("Price must be less than 10000")
        return v

    model_config = ConfigDict(str_strip_whitespace=True)
