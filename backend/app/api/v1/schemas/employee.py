from typing import Optional

from pydantic import BaseModel, Field


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


class EmployeeInDBBase(EmployeeBase):
    id: int

    model_config = {"from_attributes": True}


class Employee(EmployeeInDBBase):
    pass


class EmployeeWithDetails(EmployeeInDBBase):
    department_name: str
