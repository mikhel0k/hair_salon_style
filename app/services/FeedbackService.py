from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Feedback
from app.schemas.Feedback import FeedbackCreate, SmallFeedbackResponse
from app.repositories import FeedbackRepository


async def create_feedback(
        feedback: FeedbackCreate,
        session: AsyncSession,
):
    feedback = Feedback(**feedback.model_dump())
    feedback_in_db = await FeedbackRepository.create_feedback(
        feedback=feedback,
        session=session
    )
    return SmallFeedbackResponse.model_validate(feedback_in_db)