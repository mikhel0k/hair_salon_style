from typing import Annotated, Optional
from datetime import time

from pydantic import Field, ConfigDict, ValidationError, model_validator

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

    @model_validator(mode="after")
    def validate(self):
        days = [
            ("monday", self.monday_start, self.monday_end),
            ("tuesday", self.tuesday_start, self.tuesday_end),
            ("wednesday", self.wednesday_start, self.wednesday_end),
            ("thursday", self.thursday_start, self.thursday_end),
            ("friday", self.friday_start, self.friday_end),
            ("saturday", self.saturday_start, self.saturday_end),
            ("sunday", self.sunday_start, self.sunday_end),
        ]

        for day, start, end in days:
            if start is not None and end is not None:
                if start > end:
                    raise ValueError(f"Start time in {day} must be before end time")
                if start < time(8, 0):
                    raise ValueError(f"Start time in {day} must be after 8 o`clock")
                if end > time(20,0):
                    raise ValueError(f"End time in {day} must be before 20 o`clock")
                if (end.hour*60 + end.minute) - (start.hour*60 + start.minute) < 120:
                    raise ValueError(f"Work time in {day} must be minimum 120 minutes")
            if (start is None) != (end is None):
                raise ValueError(f"start and end times must both be None or not None")

        return self


class ScheduleCreate(ScheduleBase):
    master_id: Annotated[int, Field(..., description="ID of the master")]


class ScheduleUpdate(ScheduleBase):
    pass


class ScheduleResponse(ScheduleBase):
    id: Annotated[int, Field(..., description="ID of the schedule")]
    master_id: Annotated[int, Field(..., description="ID of the master")]

    model_config = ConfigDict(from_attributes=True)
