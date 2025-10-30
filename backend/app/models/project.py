from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    cost = Column(Float, nullable=False, default=0.0)
    revenue = Column(Float, nullable=False, default=0.0)

    # Relationships
    department = relationship("Department", back_populates="projects")
    timesheets = relationship("Timesheet", back_populates="project", cascade="all, delete-orphan")
