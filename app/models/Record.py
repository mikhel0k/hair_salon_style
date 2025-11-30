from datetime import date, time

from sqlalchemy import Column, Integer, Date, Time, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from .Base import BaseModel


class Record(BaseModel):
    __tablename__ = 'records'
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Date: Mapped[date] = Column(Date, nullable=False, index=True)
    Time: Mapped[time] = Column(Time, nullable=False)
    status: Mapped[str] = Column(String(30), nullable=False, index=True, default='created')
    price: Mapped[float] = Column(Numeric(10, 2), nullable=False)
    notes: Mapped[str | None] = Column(Text, nullable=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="records")
