from typing import Annotated

import phonenumbers
from pydantic import BaseModel, Field, ConfigDict, field_validator


class UserSchema(BaseModel):
    phone_number: Annotated[str, Field(..., description="Phone number")]

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


class UserCreate(UserSchema):
    pass


class UserResponse(UserSchema):
    id: Annotated[int, Field(..., description="User id")]

    model_config = ConfigDict(from_attributes=True)
