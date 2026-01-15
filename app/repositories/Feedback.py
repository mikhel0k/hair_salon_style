from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, session

from app.models import Feedback, Record, Master, Service, User, Cell


async def create_feedback(
        feedback: Feedback,
        session: AsyncSession,
):
    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)
    return feedback


async def update_feedback(
        feedback: Feedback,
        session: AsyncSession
):
    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)
    return feedback


async def delete_feedback(
        feedback: Feedback,
        session: AsyncSession
):
    session.delete(feedback)
    await session.commit()


async def get_feedbacks_by_master_id(
        master_id: int,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
):
    stmt = select(Feedback).join(Record).where(Record.master_id == master_id).options(
        joinedload(Feedback.record).joinedload(Record.master),
        joinedload(Feedback.record).joinedload(Record.user)
    ).offset(skip).limit(limit)
    feedbacks = await session.execute(stmt)
    return feedbacks.scalars().all()


async def get_feedback(
        feedback_id: int,
        session: AsyncSession
):
    stmt = select(Feedback).where(Feedback.id == feedback_id).options(
            joinedload(Feedback.record).joinedload(Record.master),
            joinedload(Feedback.record).joinedload(Record.service),
            joinedload(Feedback.record).joinedload(Record.user),
            joinedload(Feedback.record).joinedload(Record.cell)
    )
    feedback = await session.execute(stmt)
    return feedback.scalar_one_or_none()
