from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, field_validator, StrictInt

from app.core.validators import name_validator


class CategoryBase(BaseModel):
    name: Annotated[str, Field(
        ...,
        max_length=60,
        min_length=3,
        description="The name of the category (only letters, spaces and hyphens allowed)",
        examples=[
            "Haircut",
            "Beard cutting",
            "Manicure"
        ]
    )]

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v):
        return name_validator(v)

    model_config = ConfigDict(str_strip_whitespace=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: Annotated[StrictInt, Field(..., ge=1, description="ID of the category")]

    model_config = ConfigDict(from_attributes=True)