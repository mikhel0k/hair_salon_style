from sqlalchemy import Column, Integer, String

from .Base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
