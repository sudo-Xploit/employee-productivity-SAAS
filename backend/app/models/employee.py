from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    salary = Column(Float, nullable=False)
    revenue_generated = Column(Float, default=0.0)

    # Relationships
    department = relationship("Department", back_populates="employees")
    timesheets = relationship("Timesheet", back_populates="employee", cascade="all, delete-orphan")
