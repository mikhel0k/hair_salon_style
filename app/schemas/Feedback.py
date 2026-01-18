from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict, StrictInt

from app.schemas.Cell import CellResponse
from app.schemas.Master import MasterResponse
from app.schemas.Record import RecordResponse
from app.schemas.Service import ServiceResponse
from app.schemas.User import UserResponse


class Feedback(BaseModel):
    record_id: Annotated[StrictInt, Field(..., ge=1, description="Record id")]
    master_estimation: Annotated[int, Field(..., strict=True, ge=1, le=5, description="Master estimation")]
    master_comment: Annotated[Optional[str], Field(None, description="Master comment")]
    salon_estimation: Annotated[int, Field(..., strict=True, ge=1, le=5, description="Salon estimation")]
    salon_comment: Annotated[Optional[str], Field(None, description="Salon comment")]

    model_config = ConfigDict(str_strip_whitespace=True)


class FeedbackCreate(Feedback):
    pass


class FeedbackUpdate(BaseModel):
    master_estimation: Annotated[Optional[int], Field(None, strict=True, ge=1, le=5, description="Master estimation")]
    master_comment: Annotated[Optional[str], Field(None, description="Master comment")]
    salon_estimation: Annotated[Optional[int], Field(None, strict=True, ge=1, le=5, description="Salon estimation")]
    salon_comment: Annotated[Optional[str], Field(None, description="Salon comment")]


class SmallFeedbackResponse(Feedback):
    id: Annotated[StrictInt, Field(..., ge=1, description="Record id")]

    model_config = ConfigDict(from_attributes=True)


class FeedbackResponse(SmallFeedbackResponse):
    record: RecordResponse
    master: MasterResponse
    User: UserResponse


class FullFeedbackResponse(FeedbackResponse):
    service: ServiceResponse
    cell: CellResponse