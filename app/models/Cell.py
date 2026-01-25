from datetime import date, time
from enum import Enum

from sqlalchemy import Integer, ForeignKey, Date, Time, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Enum as SQLEnum

from app.models import BaseModel


class AllowedCellsStatuses(str, Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"


class Cell(BaseModel):
    __tablename__ = "cells"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    master_id: Mapped[int] = mapped_column(Integer, ForeignKey("masters.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[str] = mapped_column(
        SQLEnum(AllowedCellsStatuses),
        nullable=False,
        server_default=AllowedCellsStatuses.FREE.value,
    )

    master: Mapped["Master"] = relationship("Master", back_populates="cells")
    record: Mapped["Record"] = relationship("Record", back_populates="cell")

    __table_args__ = (
        UniqueConstraint('master_id', 'date', 'time', name='uq_master_datetime'),
    )
