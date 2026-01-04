from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: Annotated[str, Field(
        ...,
        max_length=60,
        min_length=3,
        description="The name of the category"
    )]
    model_config = ConfigDict(str_strip_whitespace=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: Annotated[int, Field(..., description="ID of the category")]

    model_config = ConfigDict(from_attributes=True)