from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic import field_validator, StrictInt

from app.schemas.Specialization import SpecializationResponse
from app.core.validators import phone_validator, name_validator


class AllowedMasterStatuses(str, Enum):
    ACTIVE = "active"
    VACATION = "vacation"
    DISMISSED = "dismissed"


class MasterBase(BaseModel):
    specialization_id: Annotated[StrictInt, Field(..., ge=1, description="Specialization_id of the master")]
    name: Annotated[str, Field(
        ...,
        min_length=3,
        max_length=30,
        description="Name of the master",
        examples=[
            "Petr",
            "Ivan",
            "Valeria"
        ]
    )]
    phone: Annotated[str, Field(
        ...,
        min_length=8,
        max_length=15,
        description="Phone number of the master",
        examples=[
            "+79990001010",
            "88005553535",
            "89876543210"
        ]
    )]
    email: Annotated[EmailStr, Field(
        ...,
        min_length=8,
        max_length=50,
        description="Email address of the master",
        examples=[
            "example@mail.ru",
            "example@gmail.com",
            "example@yandex.ru"
        ]
    )]
    status: Annotated[AllowedMasterStatuses, Field(
        AllowedMasterStatuses.ACTIVE,
        description="Status of the master",
    )]

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v):
        return name_validator(v)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_number(cls, v):
        return phone_validator(v)

    model_config = ConfigDict(str_strip_whitespace=True)


class MasterCreate(MasterBase):
    pass


class MasterResponse(MasterBase):
    id: Annotated[StrictInt, Field(..., ge=1, description="ID of the master")]

    model_config = ConfigDict(from_attributes=True)


class MasterFullResponse(MasterResponse):
    specialization: SpecializationResponse = Field(..., description="Specialization of the master")


class MasterUpdate(BaseModel):
    specialization_id: Annotated[Optional[StrictInt], Field(None, ge=1, description="Specialization_id of the master")]
    name: Annotated[Optional[str], Field(
        None,
        min_length=3,
        max_length=30,
        description="Name of the master",
        examples=[
            "Petr",
            "Ivan",
            "Valeria"
        ]
    )]
    phone: Annotated[Optional[str], Field(
        None,
        min_length=8,
        max_length=15,
        description="Phone number of the master",
        examples=[
            "+79990001010",
            "88005553535",
            "89876543210"
        ]
    )]
    email: Annotated[Optional[EmailStr], Field(
        None,
        min_length=8,
        max_length=50,
        description="Email address of the master",
        examples=[
            "example@mail.ru",
            "example@gmail.com",
            "example@yandex.ru"
        ]
    )]
    status: Annotated[Optional[AllowedMasterStatuses], Field(
        None,
        description="Status of the master",
    )]

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        if v:
            return name_validator(v)
        return v

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone_number(cls, v):
        if v:
            return phone_validator(v)
        return v
