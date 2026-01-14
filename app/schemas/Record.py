from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator, StrictInt

from app.schemas.Cell import CellResponse
from app.schemas.Master import MasterResponse
from app.schemas.Service import ServiceResponseSmall


class AllowedRecordStatuses(str, Enum):
    Created = "created"
    Confirmed = "confirmed"
    Rejected = "rejected"
    Cancelled = "cancelled"


class RecordResponse(BaseModel):
    id: Annotated[StrictInt, Field(..., ge=1, description="ID of record")]
    master_id: Annotated[StrictInt, Field(..., ge=1, description="Master id of record")]
    service_id: Annotated[StrictInt, Field(..., ge=1, description="Service id of record")]
    user_id: Annotated[StrictInt, Field(..., ge=1, description="User id of record")]
    cell_id: Annotated[StrictInt, Field(..., ge=1, description="Cell id of record")]
    status: Annotated[AllowedRecordStatuses, Field(AllowedRecordStatuses.Created, description="Status of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]

    model_config = ConfigDict(from_attributes=True)


class FullRecordResponse(RecordResponse):
    master: Annotated[Optional[MasterResponse], Field(..., description="Master of record")]
    service: Annotated[Optional[ServiceResponseSmall], Field(..., description="Service of record")]
    cell: Annotated[Optional[CellResponse], Field(..., description="Cell of record")]


class RecordUpdate(BaseModel):
    master_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Master id of record")]
    service_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Service id of record")]
    user_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="User id of record")]
    cell_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Cell id of record")]
    status: Annotated[Optional[AllowedRecordStatuses], Field(None, description="Status of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]


class EditRecordStatus(BaseModel):
    id: Annotated[StrictInt, Field(..., ge=1, description="ID of record")]
    status: Annotated[AllowedRecordStatuses, Field(..., description="Status of record",)]


class EditRecordNote(BaseModel):
    id: Annotated[StrictInt, Field(..., ge=1, description="ID of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]
