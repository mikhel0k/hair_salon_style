from typing import Annotated, Optional

from pydantic import BaseModel, Field, StrictInt


class WorkerBase(BaseModel):
    master_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Master ID")]
    username: Annotated[str, Field(..., description="Username of worker")]


class WorkerCreate(WorkerBase):
    password: Annotated[str, Field(..., description="Password of worker")]


class WorkerResponse(WorkerBase):
    id: Annotated[Optional[StrictInt], Field(None, description="Worker ID")]
    is_master: Annotated[bool, Field(..., description="Is master?")]
    is_admin: Annotated[bool, Field(..., description="Is admin?")]
    is_active: Annotated[bool, Field(..., description="Is active?")]


class WorkerResponseSmall(WorkerBase):
    id: Annotated[Optional[StrictInt], Field(None, description="Worker ID")]
