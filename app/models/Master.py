from enum import Enum

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import Enum as SQLEnum

from app.models import BaseModel


class AllowedMasterStatuses(str, Enum):
    ACTIVE = "ACTIVE"
    VACATION = "VACATION"
    DISMISSED = "DISMISSED"


class Master(BaseModel):
    __tablename__ = "masters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)

    specialization_id: Mapped[int] = mapped_column(Integer, ForeignKey("specializations.id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    status: Mapped[AllowedMasterStatuses] = mapped_column(
        SQLEnum(AllowedMasterStatuses),
        nullable=False,
        server_default=AllowedMasterStatuses.ACTIVE.value
    )

    records: Mapped[list["Record"]] = relationship("Record", back_populates="master")
    specialization: Mapped["Specialization"] = relationship("Specialization", back_populates="masters")
    cells: Mapped[list["Cell"]] = relationship("Cell", back_populates="master")
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="master")
    worker: Mapped["Worker"] = relationship("Worker", back_populates="master", uselist=False)

    __table_args__ = (
        UniqueConstraint('phone', 'email'),
    )
