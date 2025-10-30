from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    budget = Column(Float, nullable=False, default=0.0)

    # Relationships
    employees = relationship("Employee", back_populates="department")
    projects = relationship("Project", back_populates="department")
