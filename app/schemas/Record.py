from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.Service import ServiceResponseSmall


class AllowedRecordStatuses(str, Enum):
    Created = "created"
    Confirmed = "confirmed"
    Rejected = "rejected"
    Cancelled = "cancelled"


class RecordResponse(BaseModel):
    id: Annotated[int, Field(..., ge=1, description="ID of record")]
    master_id: Annotated[int, Field(..., ge=1, description="Master id of record")]
    service_id: Annotated[int, Field(..., ge=1, description="Service id of record")]
    user_id: Annotated[int, Field(..., ge=1, description="User id of record")]
    cell_id: Annotated[int, Field(..., ge=1, description="Cell id of record")]
    status: Annotated[AllowedRecordStatuses, Field(AllowedRecordStatuses.Created, description="Status of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]

    model_config = ConfigDict(from_attributes=True)


class RecordUpdate(BaseModel):
    master_id: Annotated[Optional[int], Field(None, ge=1, description="Master id of record")]
    service_id: Annotated[Optional[int], Field(None, ge=1, description="Service id of record")]
    user_id: Annotated[Optional[int], Field(None, ge=1, description="User id of record")]
    cell_id: Annotated[Optional[int], Field(None, ge=1, description="Cell id of record")]
    status: Annotated[Optional[AllowedRecordStatuses], Field(None, description="Status of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]


class EditRecordStatus(BaseModel):
    id: Annotated[int, Field(..., ge=1, description="ID of record")]
    status: Annotated[AllowedRecordStatuses, Field(..., description="Status of record",)]


class EditRecordNote(BaseModel):
    id: Annotated[int, Field(..., ge=1, description="ID of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]
