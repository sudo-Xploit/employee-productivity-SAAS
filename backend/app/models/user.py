from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserRole(str, PyEnum):
    ADMIN = "admin"
    DEPARTMENT_HEAD = "department_head"
    ANALYST = "analyst"
    READ_ONLY = "read_only"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    role = Column(Enum(UserRole), default=UserRole.READ_ONLY)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)