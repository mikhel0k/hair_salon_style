from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.models import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = Column(String(60), nullable=False)

    services: Mapped[list["Service"]] = relationship("Service", back_populates="category")