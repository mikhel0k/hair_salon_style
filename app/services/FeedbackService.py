from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import Feedback
from app.schemas.Feedback import FeedbackCreate, SmallFeedbackResponse
from app.repositories import FeedbackRepository


async def create_feedback(
        feedback: FeedbackCreate,
        session: AsyncSession,
):
    feedback = Feedback(**feedback.model_dump())
    try:
        feedback_in_db = await FeedbackRepository.create_feedback(
            feedback=feedback,
            session=session
        )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Feedback with this data already exists")
    return SmallFeedbackResponse.model_validate(feedback_in_db)