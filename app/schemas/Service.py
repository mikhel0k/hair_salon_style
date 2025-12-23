from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict


class Service(BaseModel):
    name: Annotated[str, Field(..., description="Name of the service")]
    price: Annotated[float, Field(..., description="Price of the service")]
    duration: Annotated[int, Field(..., description="Duration of the service")]
    category: Annotated[str, Field(..., description="Category of the service")]
    description: Annotated[str, Field(..., description="Description of the service")]


class ServiceCreate(Service):
    pass


class ServiceResponse(Service):
    id: Annotated[int, Field(..., description="ID of the service")]

    model_config = ConfigDict(from_attributes=True)


class ServiceUpdate(BaseModel):
    name: Annotated[Optional[str], Field(..., description="Name of the service")]
    price: Annotated[Optional[float], Field(..., description="Price of the service")]
    duration: Annotated[Optional[int], Field(..., description="Duration of the service")]
    category: Annotated[Optional[str], Field(..., description="Category of the service")]
    description: Annotated[Optional[str], Field(..., description="Description of the service")]
