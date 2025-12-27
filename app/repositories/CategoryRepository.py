from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.schemas.Category import CategoryCreate


async def create_category(
        category_data: CategoryCreate,
        session: AsyncSession,
) -> Category:
    category = Category(**category_data.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def read_category(
        category_id: int,
        session: AsyncSession,
):
    category = await session.get(Category, category_id)
    return category

async def read_categories_paginate(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Category).order_by(Category.id.desc()).offset(skip).limit(limit)
    categories = await session.execute(stmt)
    return categories.scalars().all()


async def delete_category(
        category: Category,
        session: AsyncSession,
):
    await session.delete(category)
    await session.commit()
