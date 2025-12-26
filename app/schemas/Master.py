from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr
import phonenumbers
from pydantic import field_validator


ALLOWED_MASTERS_STATUSES = ["active", "vacation", "dismissed"]

class MasterBase(BaseModel):
    specialization_id: Annotated[int, Field(..., description="Specialization_id of the master")]
    name: Annotated[str, Field(..., description="Name of the master")]
    phone: Annotated[str, Field(..., description="Phone number of the master")]
    email: Annotated[EmailStr, Field(..., description="Email address of the master")]
    status: Annotated[str, Field("active", description="Status of the master")]

    @field_validator("phone", mode="before")
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

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        if v not in ALLOWED_MASTERS_STATUSES:
            raise ValueError('Invalid status')
        return v


class MasterCreate(MasterBase):
    pass


class MasterResponse(MasterBase):
    id: Annotated[int, Field(..., description="ID of the master")]

    model_config = ConfigDict(from_attributes=True)


class MasterUpdate(BaseModel):
    specialization_id: Annotated[Optional[int], Field(None, description="Specialization_id of the master")]
    phone: Annotated[Optional[str], Field(None, description="Phone number of the master")]
    email: Annotated[Optional[EmailStr], Field(None, description="Email address of the master")]
    status: Annotated[Optional[str], Field(None, description="Status of the master")]

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_number(cls, v):
        if not v:
            return v
        try:
            parsed = phonenumbers.parse(str(v), "RU")
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            raise ValueError('Invalid phone')
        except:
            raise ValueError('Invalid phone format')

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        if v is None or v in ALLOWED_MASTERS_STATUSES:
            return v
        else:
            raise ValueError('Invalid status')
