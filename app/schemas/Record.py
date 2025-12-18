from datetime import date, time
from typing import Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator

ALLOWED_STATUSES = ["created", "confirmed", "rejected", "cancelled"]

class RecordCreate(BaseModel):
    date: Annotated[date, Field(..., description="Date of record", examples=[date.today()])]
    time: Annotated[time, Field(..., description="Time of record", examples=[time(14, 30)])]
    status: Annotated[Optional[str], Field(None, max_length=30, description="Status of record", examples=ALLOWED_STATUSES)]
    price: Annotated[Optional[float], Field(None, description="Price of record", examples=[500, 1500, 1410.10])]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]
    user_id: Annotated[int, Field(..., description="User id of record")]

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Price must be greater or equal than 0")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_STATUSES:
            raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
        return v

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError("Date must be in the future")
        return v


class RecordResponse(BaseModel):
    id: Annotated[int, Field(..., description="ID of record")]
    date: Annotated[date, Field(..., description="Date of record", examples=[date.today()])]
    time: Annotated[time, Field(..., description="Time of record", examples=[time(14, 30)])]
    status: Annotated[str, Field(..., max_length=30, description="Status of record", examples=ALLOWED_STATUSES)]
    price: Annotated[float, Field(..., description="Price of record", examples=[500, 1500, 1410.10])]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]
    user_id: Annotated[int, Field(..., description="User id of record")]

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Price must be greater or equal than 0")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_STATUSES:
            raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
        return v

    model_config = ConfigDict(from_attributes=True)


class RecordUpdate(BaseModel):
    id: Annotated[int, Field(..., description="ID of record")]
    date: Annotated[Optional[date], Field(None, description="Date of record", examples=[date.today()])]
    time: Annotated[Optional[time], Field(None, description="Time of record", examples=[time(14, 30)])]
    status: Annotated[Optional[str], Field(None, description="Status of record", examples=ALLOWED_STATUSES)]
    price: Annotated[Optional[float], Field(None, description="Price of record", examples=[500, 1500, 1410.10])]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Price must be greater or equal than 0")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ALLOWED_STATUSES:
            raise ValueError(f"Status must be one of {ALLOWED_STATUSES}")
        return v

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v is not None and v < date.today():
            raise ValueError("Date must be in the future")
        return v


class EditRecordStatus(BaseModel):
    id: Annotated[int, Field(..., description="ID of record")]
    status: Annotated[Optional[str], Field(None, description="Status of record", examples=ALLOWED_STATUSES)]

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
