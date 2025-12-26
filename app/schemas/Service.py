from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict


class Service(BaseModel):
    name: Annotated[str, Field(..., description="Name of the service")]
    price: Annotated[float, Field(..., description="Price of the service")]
    duration_minutes: Annotated[int, Field(..., description="Duration of the service")]
    category_id: Annotated[int, Field(..., description="Category of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]


class ServiceCreate(Service):
    pass


class ServiceResponse(Service):
    id: Annotated[int, Field(..., description="ID of the service")]

    model_config = ConfigDict(from_attributes=True)


class ServiceResponseSmall(BaseModel):
    id: Annotated[int, Field(..., description="ID of the service")]
    name: Annotated[str, Field(..., description="Name of the service")]
    price: Annotated[Optional[float], Field(None, description="Price of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]


class ServiceUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Name of the service")]
    price: Annotated[Optional[float], Field(None, description="Price of the service")]
    duration_minutes: Annotated[Optional[int], Field(None, description="Duration of the service")]
    category_id: Annotated[Optional[int], Field(None, description="Category of the service")]
    description: Annotated[Optional[str], Field(None, description="Description of the service")]
