from sqlalchemy import Integer, String, Text, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship, Mapped
from decimal import Decimal

from app.models import BaseModel


class Service(BaseModel):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)

    records: Mapped[list["Record"]] = relationship("Record", back_populates="service")
    category: Mapped["Category"] = relationship("Category", back_populates="services")
    specializations: Mapped[list["Specialization"]] = relationship(
        "Specialization",
        secondary="specialization_services",
        back_populates="services",
    )
