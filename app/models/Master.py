from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.models import BaseModel


class Master(BaseModel):
    __tablename__ = "masters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    specialization_id: Mapped[int] = mapped_column(Integer, ForeignKey("specializations.id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default='active')

    records: Mapped[list["Record"]] = relationship("Record", back_populates="master")
    specialization: Mapped["Specialization"] = relationship("Specialization", back_populates="masters")
    cells: Mapped[list["Cell"]] = relationship("Cell", back_populates="master")
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="master")

    __table_args__ = (
        UniqueConstraint('phone', 'email'),
    )
