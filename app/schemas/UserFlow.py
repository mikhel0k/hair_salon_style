from typing import Annotated, Optional
from datetime import date, time

import phonenumbers
from pydantic import BaseModel, Field, field_validator, StrictInt
from .validators import phone_validator


class MakeRecord(BaseModel):
    phone_number: Annotated[str, Field(..., max_length=60, description="Phone number",
        examples=["+79161234567", "+78005553535", "+74951234567"])]
    master_id: Annotated[StrictInt, Field(..., ge=1, description="Master id of record")]
    service_id: Annotated[StrictInt, Field(..., ge=1, description="Service id of record")]
    cell_id: Annotated[StrictInt, Field(..., ge=1, description="Cell id of record")]
    notes: Annotated[Optional[str], Field(
        None,
        description="Notes of record",
        examples=["Customer requested morning appointment", "Special requirements"]
    )]

    @field_validator("phone_number", mode="before")
    @classmethod
    def validate_phone_number(cls, v):
        return phone_validator(v)
