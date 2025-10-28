from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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


class ProjectInDBBase(ProjectBase):
    id: int

    model_config = {"from_attributes": True}


class Project(ProjectInDBBase):
    pass


class ProjectWithTimesheets(ProjectInDBBase):
    timesheets: List[Dict[str, Any]] = []
    total_hours: float = 0.0


class ProjectWithDetails(ProjectInDBBase):
    department_name: str
    profit: float = 0.0
    profit_margin: float = 0.0
