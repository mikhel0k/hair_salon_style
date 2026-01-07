from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)

    services: Mapped[list["Service"]] = relationship("Service", back_populates="category")
