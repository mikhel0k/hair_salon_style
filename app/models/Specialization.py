from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.models import BaseModel


class Specialization(BaseModel):
    __tablename__ = 'specializations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)

    masters: Mapped[list["Master"]] = relationship("Master", back_populates="specialization")
    services: Mapped[list["Service"]] = relationship(
        "Service",
        back_populates="specializations",
        secondary="specialization_services"
    )
