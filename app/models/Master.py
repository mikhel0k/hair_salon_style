from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, relationship

from app.models import BaseModel


class Master(BaseModel):
    __tablename__ = "masters"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = Column(String, nullable=False)
    specialization: Mapped[str] = Column(String, nullable=False)
    phone: Mapped[str] = Column(String, nullable=False)
    email: Mapped[str] = Column(String, nullable=False)
    work_schedule: Mapped[str] = Column(String, nullable=False)
    status: Mapped[str] = Column(String, nullable=False)

    records: Mapped["Record"] = relationship("Record", back_populates="master")