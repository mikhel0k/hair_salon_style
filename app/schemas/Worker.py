from typing import Annotated, Optional

from pydantic import BaseModel, Field, StrictInt


class WorkerBase(BaseModel):
    master_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Master ID")]
    username: Annotated[str, Field(..., min_length=3, max_length=30, description="Username of worker")]


class WorkerCreate(WorkerBase):
    password: Annotated[str, Field(..., min_length=8, max_length=30, description="Password of worker")]
    is_master: Annotated[bool, Field(..., strict=True, description="Is master?")]
    is_admin: Annotated[bool, Field(..., strict=True, description="Is admin?")]
    is_active: Annotated[bool, Field(..., strict=True, description="Is active?")]


class Login(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=30, description="Username of worker")]
    password: Annotated[str, Field(..., min_length=8, max_length=30, description="Password of worker")]
