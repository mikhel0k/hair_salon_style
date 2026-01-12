from typing import Annotated, Optional

from pydantic import BaseModel, Field, StrictInt, ConfigDict

from app.schemas.Master import MasterResponse


class WorkerBase(BaseModel):
    master_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Master ID")]
    username: Annotated[str, Field(..., description="Username of worker")]


class WorkerCreate(WorkerBase):
    password: Annotated[str, Field(..., description="Password of worker")]
    is_master: Annotated[bool, Field(..., description="Is master?")]
    is_admin: Annotated[bool, Field(..., description="Is admin?")]
    is_active: Annotated[bool, Field(..., description="Is active?")]


class WorkerResponseInner(WorkerBase):
    id: Annotated[Optional[StrictInt], Field(None, description="Worker ID")]
    password: Annotated[str, Field(..., description="Password of worker")]
    is_master: Annotated[bool, Field(..., description="Is master?")]
    is_admin: Annotated[bool, Field(..., description="Is admin?")]
    is_active: Annotated[bool, Field(..., description="Is active?")]

    model_config = ConfigDict(from_attributes=True)


class WorkerResponse(WorkerBase):
    id: Annotated[Optional[StrictInt], Field(None, description="Worker ID")]
    master: Annotated[Optional[MasterResponse], Field(None, description="Master ID")]

    model_config = ConfigDict(from_attributes=True)
