from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated

from app.schemas.Cell import CellResponse
from app.schemas.Master import MasterResponse
from app.schemas.Record import RecordResponse
from app.schemas.Service import ServiceResponse
from app.schemas.User import UserResponse


class Feedback(BaseModel):
    record_id: Annotated[int, Field(..., description="Record id")]
    master_estimation: Annotated[int, Field(..., description="Master estimation")]
    master_comment: Annotated[Optional[str], Field(None, description="Master comment")]
    salon_estimation: Annotated[int, Field(..., description="Salon estimation")]
    salon_comment: Annotated[Optional[str], Field(None, description="Salon comment")]


class FeedbackCreate(Feedback):
    pass


class FeedbackUpdate(BaseModel):
    master_estimation: Annotated[Optional[int], Field(None, description="Master estimation")]
    master_comment: Annotated[Optional[str], Field(None, description="Master comment")]
    salon_estimation: Annotated[Optional[int], Field(None, description="Salon estimation")]
    salon_comment: Annotated[Optional[str], Field(None, description="Salon comment")]


class FeedbackResponse(Feedback):
    id: Annotated[int, Field(..., description="Record id")]
    record: RecordResponse
    master: MasterResponse
    User: UserResponse


class FullFeedbackResponse(FeedbackResponse):
    service: ServiceResponse
    cell: CellResponse