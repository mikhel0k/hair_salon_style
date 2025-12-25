from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict


class MasterBase(BaseModel):
    name: Annotated[str, Field(..., description="Name of the master")]
    specialization: Annotated[str, Field(..., description="Specialization of the master")]
    phone: Annotated[str, Field(..., description="Phone number of the master")]
    email: Annotated[str, Field(..., description="Email address of the master")]
    work_schedule: Annotated[str, Field(..., description="Work schedule of the master")]
    status: Annotated[str, Field("hired", description="Status of the master")]


class MasterCreate(MasterBase):
    pass


class MasterResponse(MasterBase):
    id: Annotated[int, Field(..., description="ID of the master")]

    model_config = ConfigDict(from_attributes=True)


class MasterUpdate(BaseModel):
    name: Annotated[Optional[str], Field(..., description="Name of the master")]
    specialization: Annotated[Optional[str], Field(..., description="Specialization of the master")]
    phone: Annotated[Optional[str], Field(..., description="Phone number of the master")]
    email: Annotated[Optional[str], Field(..., description="Email address of the master")]
    work_schedule: Annotated[Optional[str], Field(..., description="Work schedule of the master")]
    status: Annotated[Optional[str], Field(..., description="Status of the master")]