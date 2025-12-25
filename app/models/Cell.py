from sqlalchemy import Column, Integer, ForeignKey, Date, Time, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from datetime import date, time

from app.models import BaseModel


class Cell(BaseModel):
    __tablename__ = "cells"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    master_id: Mapped[int] = Column(Integer, ForeignKey("masters.id"), nullable=False)
    date: Mapped[date] = Column(Date, nullable=False)
    time: Mapped[time] = Column(Time, nullable=False)
    status: Mapped[str] = Column(String(30), nullable=False, server_default="free")

    master: Mapped["Master"] = relationship("Master", back_populates="cells")
    record: Mapped["Record"] = relationship("Record", back_populates="cell")

    __table_args__ = (
        UniqueConstraint('master_id', 'date', 'time', name='uq_master_datetime'),
    )