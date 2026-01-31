from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.User import UserCreate, UserFind
from app.models.User import User


async def create_user(
        session: AsyncSession,
        user: UserCreate
) -> User:
    user_info = User(**user.model_dump())
    session.add(user_info)
    await session.flush()
    await session.refresh(user_info)
    return user_info


async def read_user_by_phone(
        user: UserFind,
        session: AsyncSession,
) -> User:
    stmt = select(User).where(User.phone_number == user.phone_number)
    answ = await session.execute(stmt)
    user_info = answ.scalar_one_or_none()
    return user_info


async def read_user_by_id(
        user_id: int,
        session: AsyncSession,
):
    user = await session.get(User, user_id)
    return user
