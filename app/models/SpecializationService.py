from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped

from app.models import BaseModel


class SpecializationService(BaseModel):
    __tablename__ = 'specialization_services'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    specialization_id: Mapped[int] = Column(Integer, ForeignKey('specializations.id'), nullable=False)
    service_id: Mapped[int] = Column(Integer, ForeignKey('services.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('specialization_id', 'service_id', name='uq_specialization_service'),
    )
