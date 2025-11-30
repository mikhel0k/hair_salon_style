from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserResponse, UserFind
from app.models.User import User


async def create_user(
        session: AsyncSession,
        user: UserCreate
) -> UserResponse:
    stmt = select(User).where(User.phone_number == user.phone_number)
    answ = await session.execute(stmt)
    check_info = answ.scalar_one_or_none()
    if check_info:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    user_info = User(**user.model_dump())
    session.add(user_info)
    await session.commit()
    await session.refresh(user_info)
    return UserResponse.model_validate(user_info)


async def get_user_by_phone(
        user: UserFind,
        session: AsyncSession,
) -> UserResponse:
    stmt = select(User).where(User.phone_number == user.phone_number)
    answ = await session.execute(stmt)
    user_info = answ.scalar_one_or_none()
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user_info)
