from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    name: str
    budget: float = Field(..., ge=0)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    budget: Optional[float] = Field(None, ge=0)


class DepartmentInDBBase(DepartmentBase):
    id: int

    model_config = {"from_attributes": True}


class Department(DepartmentInDBBase):
    pass


class DepartmentWithEmployees(DepartmentInDBBase):
    employees: List[Dict[str, Any]] = []


class DepartmentWithProjects(DepartmentInDBBase):
    projects: List[Dict[str, Any]] = []


class DepartmentWithDetails(DepartmentInDBBase):
    employees: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    total_salary_cost: float = 0.0
    total_revenue: float = 0.0
    profit_margin: float = 0.0
