from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.models import BaseModel


class Master(BaseModel):
    __tablename__ = "masters"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)


    specialization_id: Mapped[int] = Column(Integer, ForeignKey("specializations.id"))
    name: Mapped[str] = Column(String(30), nullable=False)
    phone: Mapped[str] = Column(String(15), nullable=False)
    email: Mapped[str] = Column(String(50), nullable=False)
    status: Mapped[str] = Column(String(30), nullable=False, default='active')

    records: Mapped[list["Record"]] = relationship("Record", back_populates="master")
    specialization: Mapped["Specialization"] = relationship(
        "Specialization",
        back_populates="masters",
        lazy="joined"
    )
    cells: Mapped[list["Cell"]] = relationship("Cell", back_populates="master")
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="master")
