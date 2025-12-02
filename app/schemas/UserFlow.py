from typing import Annotated, Optional
from datetime import date, time

import phonenumbers
from pydantic import BaseModel, Field, field_validator


class MakeRecord(BaseModel):
    phone_number: Annotated[str, Field(..., description="Phone number",
        examples=["+79161234567", "+78005553535", "+74951234567"])]
    date: Annotated[date, Field(..., description="Date of record", examples=[date.today()])]
    time: Annotated[time, Field(..., description="Time of record", examples=[time(14, 30)])]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]

    @field_validator("phone_number", mode="before")
    @classmethod
    def validate_phone_number(cls, v):
        if not v:
            raise ValueError("phone_number cannot be empty")

        try:
            parsed = phonenumbers.parse(str(v), "RU")
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            raise ValueError('Invalid phone')
        except:
            raise ValueError('Invalid phone format')

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError("Date must be in the future")
        return v
