from datetime import date
from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Timesheet(Base):
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    hours_worked = Column(Float, nullable=False)
    date = Column(Date, nullable=False, default=date.today)

    # Relationships
    employee = relationship("Employee", back_populates="timesheets")
    project = relationship("Project", back_populates="timesheets")
