from typing import Annotated, Optional
from datetime import time

from pydantic import Field, ConfigDict

from app.models import BaseModel


class ScheduleBase(BaseModel):
    monday_start: Annotated[Optional[time], Field(None, description="Monday start time")]
    monday_end: Annotated[Optional[time], Field(None, description="Monday end time")]
    tuesday_start: Annotated[Optional[time], Field(None, description="Tuesday start time")]
    tuesday_end: Annotated[Optional[time], Field(None, description="Tuesday end time")]
    wednesday_start: Annotated[Optional[time], Field(None, description="Wednesday start time")]
    wednesday_end: Annotated[Optional[time], Field(None, description="Wednesday end time")]
    thursday_start: Annotated[Optional[time], Field(None, description="Thursday start time")]
    thursday_end: Annotated[Optional[time], Field(None, description="Thursday end time")]
    friday_start: Annotated[Optional[time], Field(None, description="Friday start time")]
    friday_end: Annotated[Optional[time], Field(None, description="Friday end time")]
    saturday_start: Annotated[Optional[time], Field(None, description="Saturday start time")]
    saturday_end: Annotated[Optional[time], Field(None, description="Saturday end time")]
    sunday_start: Annotated[Optional[time], Field(None, description="Sunday start time")]
    sunday_end: Annotated[Optional[time], Field(None, description="Sunday end time")]


class ScheduleCreate(ScheduleBase):
    master_id: Annotated[int, Field(..., description="ID of the master")]


class ScheduleUpdate(ScheduleBase):
    pass


class ScheduleResponse(ScheduleBase):
    id: Annotated[int, Field(..., description="ID of the schedule")]
    master_id: Annotated[int, Field(..., description="ID of the master")]

    model_config = ConfigDict(from_attributes=True)
