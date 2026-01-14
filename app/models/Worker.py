from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.Base import BaseModel


class Worker(BaseModel):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    master_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("masters.id"), nullable=True, unique=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    is_master: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    master: Mapped["Master"] = relationship("Master", back_populates="worker")