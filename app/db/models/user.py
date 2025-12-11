from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.constants import Role
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
