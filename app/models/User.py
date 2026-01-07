from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.models import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False, unique=True, index=True)

    records: Mapped[list["Record"]] = relationship("Record", back_populates="user")
