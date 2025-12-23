from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import Mapped, relationship

from .Base import BaseModel


class Service(BaseModel):
    __tablename__ = "services"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = Column(String, nullable=False)
    price: Mapped[float] = Column(Float, nullable=False)
    duration: Mapped[int] = Column(Integer, nullable=False)
    category: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)

    records: Mapped["Record"] = relationship("Record", back_populates="service")
