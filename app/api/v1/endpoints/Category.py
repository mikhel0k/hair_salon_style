from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Category import CategoryResponse, CategoryCreate
from app.core import get_session
from app.services import CategoryService
from app.core.dependencies import is_user_admin

router = APIRouter()


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
        category_data: CategoryCreate,
        admin_user = Depends(is_user_admin),
        session = Depends(get_session),
):
    return await CategoryService.create_category(
        session=session,
        category=category_data,
    )


@router.get(
    "/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
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


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
        category_id: int,
        admin_user = Depends(is_user_admin),
        session = Depends(get_session),
):
    await CategoryService.delete_category(
        category_id=category_id,
        session=session,
    )
