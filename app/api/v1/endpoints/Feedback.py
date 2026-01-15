from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_session
from app.schemas.Feedback import SmallFeedbackResponse, FeedbackCreate, FeedbackResponse
from app.services import FeedbackService

router = APIRouter()


@router.post("/")
async def create_feedback(
        feedback: FeedbackCreate,
        session: AsyncSession = Depends(get_session)
):
    return await FeedbackService.create_feedback(
        feedback=feedback,
        session=session
    )