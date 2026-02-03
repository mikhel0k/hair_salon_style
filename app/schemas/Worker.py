from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, StrictInt, EmailStr
from pydantic import field_validator

from app.core.validators import phone_validator


class WorkerBase(BaseModel):
    master_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Master ID")]
    username: Annotated[str, Field(..., min_length=3, max_length=30, description="Username of worker")]
    phone: Annotated[str, Field(
        ...,
        min_length=8,
        max_length=15,
        description="Phone number of the worker",
        examples=["+79990001010", "88005553535", "89876543210"],
    )]
    email: Annotated[EmailStr, Field(
        ...,
        min_length=8,
        max_length=50,
        description="Email address of the worker",
        examples=["example@mail.ru", "example@gmail.com", "example@yandex.ru"],
    )]

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_number(cls, v):
        return phone_validator(v)

    model_config = ConfigDict(str_strip_whitespace=True)


class WorkerCreate(WorkerBase):
    password: Annotated[str, Field(..., min_length=8, max_length=30, description="Password of worker")]
    is_master: Annotated[bool, Field(..., strict=True, description="Is master?")]
    is_admin: Annotated[bool, Field(..., strict=True, description="Is admin?")]
    is_active: Annotated[bool, Field(..., strict=True, description="Is active?")]


class Login(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=30, description="Username of worker")]
    password: Annotated[str, Field(..., min_length=8, max_length=30, description="Password of worker")]


class LoginConfirm(BaseModel):
    code: Annotated[str, Field(..., min_length=6, max_length=6, description="Code of login confirmation")]
    jti: Annotated[str, Field(..., description="JTI of login confirmation")]