from typing import Annotated
from datetime import date, time

from pydantic import BaseModel, Field, ConfigDict


class CellBase(BaseModel):
    master_id: Annotated[int, Field(..., description="ID of the master")]
    date: Annotated[date, Field(..., description="Date of the cell")]
    time: Annotated[time, Field(..., description="Time of the cell")]
    status: Annotated[str, Field(..., max_length=30, description="Status of the cell")]


class CellCreate(CellBase):
    pass


class CellResponse(CellBase):
    id: Annotated[int, Field(..., description="ID of the cell")]

    model_config = ConfigDict(from_attributes=True)
