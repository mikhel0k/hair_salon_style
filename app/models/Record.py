from enum import Enum

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import Enum as SQLEnum

from app.models import BaseModel


class AllowedRecordStatuses(str, Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Record(BaseModel):
    __tablename__ = 'records'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    master_id: Mapped[int] = mapped_column(Integer, ForeignKey('masters.id'), nullable=False)
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey('services.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    cell_id: Mapped[int] = mapped_column(Integer, ForeignKey('cells.id'), nullable=False)
    status: Mapped[AllowedRecordStatuses] = mapped_column(
        SQLEnum(AllowedRecordStatuses),
        nullable=False,
        server_default=AllowedRecordStatuses.CREATED.value
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="records")
    service: Mapped["Service"] = relationship("Service", back_populates="records")
    master: Mapped["Master"] = relationship("Master", back_populates="records")
    cell: Mapped["Cell"] = relationship("Cell", back_populates="record")
