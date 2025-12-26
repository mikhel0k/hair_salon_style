from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.Service import ServiceResponseSmall

ALLOWED_STATUSES = ["created", "confirmed", "rejected", "cancelled"]

class RecordCreate(BaseModel):
    master_id: Annotated[int, Field(..., description="Master id of record")]
    service_id: Annotated[int, Field(..., description="Service id of record")]
    user_id: Annotated[int, Field(..., description="User id of record")]
    cell_id: Annotated[int, Field(..., description="Cell id of record")]
    status: Annotated[Optional[str], Field(None, max_length=30, description="Status of record", examples=ALLOWED_STATUSES)]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_STATUSES:
            raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
        return v


class RecordResponse(BaseModel):
    id: Annotated[int, Field(..., description="ID of record")]
    master_id: Annotated[int, Field(..., description="Master id of record")]
    service_id: Annotated[int, Field(..., description="Service id of record")]
    user_id: Annotated[int, Field(..., description="User id of record")]
    cell_id: Annotated[int, Field(..., description="Cell id of record")]
    status: Annotated[str, Field(..., max_length=30, description="Status of record", examples=ALLOWED_STATUSES)]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]
    price: Annotated[float, Field(..., description="Price of the service")]
    name: Annotated[str, Field(..., max_length=30, description="Name of the master")]

    service: Annotated[ServiceResponseSmall, Field(..., description="Service response")]

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_STATUSES:
            raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
        return v

    model_config = ConfigDict(from_attributes=True)


class RecordUpdate(BaseModel):
    id: Annotated[int, Field(..., description="ID of record")]
    master_id: Annotated[Optional[int], Field(None, description="Master id of record")]
    service_id: Annotated[Optional[int], Field(None, description="Service id of record")]
    user_id: Annotated[int, Field(..., description="User id of record")]
    cell_id: Annotated[int, Field(..., description="Cell id of record")]
    status: Annotated[Optional[str], Field(None, max_length=30, description="Status of record", examples=ALLOWED_STATUSES)]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ALLOWED_STATUSES:
            raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
        return v


class EditRecordStatus(BaseModel):
    id: Annotated[int, Field(..., description="ID of record")]
    status: Annotated[Optional[str], Field(None, max_length=30, description="Status of record", examples=ALLOWED_STATUSES)]

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ALLOWED_STATUSES:
            raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
        elif v is None:
            raise ValueError("Status is None")
        return v


class EditRecordNote(BaseModel):
    id: Annotated[int, Field(..., description="ID of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]
