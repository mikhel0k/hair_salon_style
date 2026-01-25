from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Category import CategoryCreate, CategoryResponse
from app.repositories import CategoryRepository


async def create_category(
        category: CategoryCreate,
        session: AsyncSession,
):
    try:
        category_from_db = await CategoryRepository.create_category(
            category_data=category,
            session=session,
        )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Category with this data already exists")
    category_data = CategoryResponse.model_validate(category_from_db)
    return category_data


async def get_category_by_id(
        category_id: int,
        session: AsyncSession
):
    category_from_db = await CategoryRepository.read_category(
        category_id=category_id,
        session=session,
    )
    if not category_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_data = CategoryResponse.model_validate(category_from_db)
    return category_data


async def get_categories_paginated(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    categories_from_db = await CategoryRepository.read_categories_paginate(
        skip=skip,
        limit=limit,
        session=session,
    )
    categories_data = [CategoryResponse.model_validate(category) for category in categories_from_db]
    return categories_data


async def delete_category(
        category_id: int,
        session: AsyncSession,
):
    category_from_db = await CategoryRepository.read_category(
        category_id=category_id,
        session=session,
    )
    if not category_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    try:
        await CategoryRepository.delete_category(
            category=category_from_db,
            session=session
        )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Something went wrong")
