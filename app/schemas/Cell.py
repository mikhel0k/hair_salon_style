from typing import Annotated
from datetime import date, time, datetime, timedelta

from pydantic import BaseModel, Field, ConfigDict, field_validator
from enum import Enum
from .validators import date_validator

class AllowedCellsStatuses(str, Enum):
    FREE = "free"
    OCCUPIED = "occupied"


class CellBase(BaseModel):
    master_id: Annotated[int, Field(..., ge=1, description="ID of the master")]
    date: Annotated[date, Field(
        ...,
        description="Date of the cell",
        examples=[
            datetime.today(),
            datetime.today() + timedelta(days=2),
            datetime.today() + timedelta(days=7),
        ]
    )]
    time: Annotated[time, Field(
        ...,
        description="Time of the cell",
        examples=[
            time(hour=8, minute=00),
            time(hour=9, minute=15),
            time(hour=11, minute=30),
        ]
    )]
    status: Annotated[AllowedCellsStatuses, Field(
        default=AllowedCellsStatuses.FREE,
        description="Status of the cell",
    )]

    model_config = ConfigDict(str_strip_whitespace=True)


class CellCreate(CellBase):
    @field_validator("date", mode="after")
    @classmethod
    def validate_date(cls, v):
        return date_validator(v)



class CellResponse(CellBase):
    id: Annotated[int, Field(..., ge=1, description="ID of the cell")]

    model_config = ConfigDict(from_attributes=True)
