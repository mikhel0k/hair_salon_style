from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Category import CategoryResponse, CategoryCreate
from app.core import get_session
from app.services import CategoryService

router = APIRouter()


@router.post("/", response_model=CategoryResponse)
async def create_category(
        category_data: CategoryCreate,
        session = Depends(get_session),
):
    return await CategoryService.create_category(
        session=session,
        category=category_data,
    )


@router.get("/")
async def get_categories(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_session),
):
    return await CategoryService.get_categories_paginated(
        session=session,
        skip=skip,
        limit=limit,
    )


# @router.get("/{category_id}", response_model=CategoryResponse)
# async def get_category(
#         category_id: int,
#         session = Depends(get_session)
# ):
#     return await CategoryService.get_category_by_id(
#         session=session,
#         category_id=category_id
#     )


@router.delete("/{category_id}")
async def delete_category(
        category_id: int,
        session = Depends(get_session),
):
    await CategoryService.delete_category(category_id=category_id, session=session)
    return {"status": "success"}
