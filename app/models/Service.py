from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.models import BaseModel


class Service(BaseModel):
    __tablename__ = "services"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = Column(String(60), nullable=False)
    price: Mapped[float] = Column(DECIMAL(10, 2), nullable=False)
    duration_minutes: Mapped[int] = Column(Integer, nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    category_id: Mapped[int] = Column(Integer, ForeignKey("categories.id"), nullable=False)

    records: Mapped[list["Record"]] = relationship("Record", back_populates="service")
    category: Mapped["Category"] = relationship("Category", back_populates="services")
    specializations: Mapped[list["Specialization"]] = relationship(
        "Specialization",
        secondary="specialization_services",
        back_populates="services",
    )
