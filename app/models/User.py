from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .Base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phone_number: Mapped[str] = Column(String(20), nullable=False, unique=True, index=True)

    records: Mapped[list["Record"]] = relationship("Record", back_populates="user")
