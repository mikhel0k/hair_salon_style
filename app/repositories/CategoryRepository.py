from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.schemas.Category import CategoryCreate
import logging

logger = logging.getLogger(__name__)


async def create_category(
        category_data: CategoryCreate,
        session: AsyncSession,
) -> Category:
    category = Category(**category_data.model_dump())
    session.add(category)
    await session.flush()
    await session.refresh(category)
    logger.info("Category created: id=%s, name=%s", category.id, category.name)
    return category


async def read_category(
        category_id: int,
        session: AsyncSession,
):
    category = await session.get(Category, category_id)
    logger.debug("Category read: id=%s, name=%s", category.id, category.name)
    return category

async def read_categories_paginate(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Category).order_by(Category.id.asc()).offset(skip).limit(limit)
    result = await session.execute(stmt)
    items = result.scalars().all()
    logger.debug("Categories read: skip=%s, limit=%s, count=%s", skip, limit, len(items))
    return items


async def delete_category(
        category: Category,
        session: AsyncSession,
):
    cat_id, cat_name = category.id, category.name
    await session.delete(category)
    await session.flush()
    logger.info("Category deleted: id=%s, name=%s", cat_id, cat_name)
