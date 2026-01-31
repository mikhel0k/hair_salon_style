import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.Category import CategoryCreate, CategoryResponse
from app.repositories import CategoryRepository

logger = logging.getLogger(__name__)


async def create_category(
        category: CategoryCreate,
        session: AsyncSession,
):
    logger.debug("create_category: name=%s", category.name)
    try:
        category_from_db = await CategoryRepository.create_category(
            category_data=category,
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("create_category: conflict, name=%s", category.name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this data already exists",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("create_category: unexpected error, name=%s", category.name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Category created: id=%s, name=%s", category_from_db.id, category_from_db.name)
    return CategoryResponse.model_validate(category_from_db)


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
    return [CategoryResponse.model_validate(c) for c in categories_from_db]


async def delete_category(
        category_id: int,
        session: AsyncSession,
):
    logger.debug("delete_category: category_id=%s", category_id)
    category_from_db = await CategoryRepository.read_category(
        category_id=category_id,
        session=session,
    )
    if not category_from_db:
        logger.info("delete_category: not found, category_id=%s", category_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    try:
        await CategoryRepository.delete_category(
            category=category_from_db,
            session=session,
        )
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.info("delete_category: conflict, category_id=%s", category_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Something went wrong",
        )
    except Exception as e:
        await session.rollback()
        logger.exception("delete_category: unexpected error, category_id=%s", category_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
    logger.info("Category deleted: id=%s, name=%s", category_from_db.id, category_from_db.name)
