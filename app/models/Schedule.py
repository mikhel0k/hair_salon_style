from datetime import time

from sqlalchemy import Integer, Column, ForeignKey, Time
from sqlalchemy.orm import Mapped, relationship

from app.models import BaseModel


class Schedule(BaseModel):
    __tablename__ = "schedules"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    master_id: Mapped[int] = Column(Integer, ForeignKey("masters.id"), unique=True, nullable=False)

    monday_start: Mapped[time] = Column(Time, nullable=True)
    monday_end: Mapped[time] = Column(Time, nullable=True)

    tuesday_start: Mapped[time] = Column(Time, nullable=True)
    tuesday_end: Mapped[time] = Column(Time, nullable=True)

    wednesday_start: Mapped[time] = Column(Time, nullable=True)
    wednesday_end: Mapped[time] = Column(Time, nullable=True)

    thursday_start: Mapped[time] = Column(Time, nullable=True)
    thursday_end: Mapped[time] = Column(Time, nullable=True)

    friday_start: Mapped[time] = Column(Time, nullable=True)
    friday_end: Mapped[time] = Column(Time, nullable=True)

    saturday_start: Mapped[time] = Column(Time, nullable=True)
    saturday_end: Mapped[time] = Column(Time, nullable=True)

    sunday_start: Mapped[time] = Column(Time, nullable=True)
    sunday_end: Mapped[time] = Column(Time, nullable=True)

    master: Mapped["Master"] = relationship("Master", back_populates="schedule")
