from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class Feedback(BaseModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, ForeignKey("records.id"), nullable=False)
    master_estimation: Mapped[int] = mapped_column(Integer, nullable=False)
    master_comment: Mapped[str] = mapped_column(Text, nullable=True)
    salon_estimation: Mapped[int] = mapped_column(Integer, nullable=False)
    salon_comment: Mapped[str] = mapped_column(Text, nullable=True)
