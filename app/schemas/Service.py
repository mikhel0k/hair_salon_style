from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class Service(BaseModel):
    name: Annotated[str, Field(..., max_length=60, description="Name of the service")]
    price: Annotated[float, Field(..., description="Price of the service")]
    duration_minutes: Annotated[int, Field(..., description="Duration of the service")]
    category_id: Annotated[int, Field(..., description="Category of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]

    @field_validator("duration_minutes")
    @classmethod
    def validate_duration_minutes(cls, v):
        if v <= 0:
            raise ValueError("Duration must be greater than 0")
        if v > 180:
            raise ValueError("Duration must be less than 3 hours")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v


class ServiceCreate(Service):
    pass


class ServiceResponse(Service):
    id: Annotated[int, Field(..., description="ID of the service")]

    model_config = ConfigDict(from_attributes=True)


class ServiceResponseSmall(BaseModel):
    id: Annotated[int, Field(..., description="ID of the service")]
    name: Annotated[str, Field(..., max_length=60, description="Name of the service")]
    price: Annotated[float, Field(..., description="Price of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    model_config = ConfigDict(from_attributes=True)


class ServiceUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, max_length=60, description="Name of the service")]
    price: Annotated[Optional[float], Field(None, description="Price of the service")]
    duration_minutes: Annotated[Optional[int], Field(None, description="Duration of the service")]
    category_id: Annotated[Optional[int], Field(None, description="Category of the service")]
    description: Annotated[Optional[str], Field(None, description="Description of the service")]

    @field_validator("duration_minutes")
    @classmethod
    def validate_duration_minutes(cls, v):
        if v <= 0:
            raise ValueError("Duration must be greater than 0")
        if v > 180:
            raise ValueError("Duration must be less than 3 hours")
        return v


    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v
