"""
Base schemas for all entities to avoid circular imports.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# Base schemas for Department
class DepartmentBase(BaseModel):
    name: str
    budget: float = Field(..., ge=0)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    budget: Optional[float] = Field(None, ge=0)


# Base schemas for Employee
class EmployeeBase(BaseModel):
    name: str
    department_id: int
    salary: float = Field(..., gt=0)
    revenue_generated: Optional[float] = 0.0


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None
    salary: Optional[float] = Field(None, gt=0)
    revenue_generated: Optional[float] = None


# Base schemas for Project
class ProjectBase(BaseModel):
    name: str
    department_id: int
    cost: float = Field(..., ge=0)
    revenue: float = Field(..., ge=0)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None
    cost: Optional[float] = Field(None, ge=0)
    revenue: Optional[float] = Field(None, ge=0)


# Base schemas for Timesheet
class TimesheetBase(BaseModel):
    employee_id: int
    project_id: int
    hours_worked: float = Field(..., gt=0)
    date: Optional[str] = None


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetUpdate(BaseModel):
    employee_id: Optional[int] = None
    project_id: Optional[int] = None
    hours_worked: Optional[float] = Field(None, gt=0)
    date: Optional[str] = None
