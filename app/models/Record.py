from datetime import date, time

from sqlalchemy import Column, Integer, Date, Time, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.models import BaseModel


class Record(BaseModel):
    __tablename__ = 'records'
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date: Mapped[date] = Column(Date, nullable=False, index=True)
    time: Mapped[time] = Column(Time, nullable=False)
    status: Mapped[str] = Column(String(30), nullable=False, index=True, default='created')
    price: Mapped[float] = Column(Numeric(10, 2), nullable=False, default=0.0)
    notes: Mapped[str | None] = Column(Text, nullable=True)

    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    service_id: Mapped[int] = Column(Integer, ForeignKey('services.id'), nullable=False)
    master_id: Mapped[int] = Column(Integer, ForeignKey('masters.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="records")
    service: Mapped["Service"] = relationship("Service", back_populates="records")
    master: Mapped["Master"] = relationship("Master", back_populates="records")
