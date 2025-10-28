from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class TimesheetBase(BaseModel):
    employee_id: int
    project_id: int
    hours_worked: float = Field(..., gt=0)
    date: date = Field(default_factory=date.today)


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetUpdate(BaseModel):
    employee_id: Optional[int] = None
    project_id: Optional[int] = None
    hours_worked: Optional[float] = Field(None, gt=0)
    date: Optional[date] = None


class TimesheetInDBBase(TimesheetBase):
    id: int

    model_config = {"from_attributes": True}


class Timesheet(TimesheetInDBBase):
    pass


class TimesheetWithDetails(TimesheetInDBBase):
    employee_name: str
    project_name: str
    department_name: str
