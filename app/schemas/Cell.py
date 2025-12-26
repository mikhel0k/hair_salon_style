from typing import Annotated
from datetime import date, time

from pydantic import BaseModel, Field, ConfigDict, field_validator

ALLOWED_CELLS_STATUSES = ["free", "occupied"]


class CellBase(BaseModel):
    master_id: Annotated[int, Field(..., description="ID of the master")]
    date: Annotated[date, Field(..., description="Date of the cell")]
    time: Annotated[time, Field(..., description="Time of the cell")]
    status: Annotated[str, Field(..., max_length=30, description="Status of the cell")]


    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_CELLS_STATUSES:
            raise ValueError("Status cannot be not free or occupied")
        return v


class CellCreate(CellBase):
    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v is None:
            raise ValueError("Date cannot be null")
        if v < date.today():
            raise ValueError("Date cannot be in the past")
        return v


class CellResponse(CellBase):
    id: Annotated[int, Field(..., description="ID of the cell")]

    model_config = ConfigDict(from_attributes=True)
