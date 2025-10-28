from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_analyst_permission, get_department_head_permission
from app.db.session import get_db
from app.models.user import User
from app.services import analytics_service, department_service, employee_service, project_service

router = APIRouter()


@router.get("/company", response_model=Dict)
def get_company_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get overall company analytics.
    """
    return analytics_service.get_company_analytics(db)


@router.get("/departments/{department_id}", response_model=Dict)
def get_department_analytics(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get analytics for a specific department.
    """
    department = department_service.get(db, department_id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    return analytics_service.get_department_analytics(db, department_id)


@router.get("/projects/{project_id}", response_model=Dict)
def get_project_analytics(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get analytics for a specific project.
    """
    project = project_service.get(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return analytics_service.get_project_analytics(db, project_id)


@router.get("/employees/{employee_id}", response_model=Dict)
def get_employee_analytics(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get analytics for a specific employee.
    """
    employee = employee_service.get(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return analytics_service.get_employee_analytics(db, employee_id)


@router.get("/top-performers", response_model=List[Dict])
def get_top_performers(
    db: Session = Depends(get_db),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get top performing employees based on revenue generated.
    """
    return analytics_service.get_top_performers(db, limit)


@router.get("/top-projects", response_model=List[Dict])
def get_top_projects(
    db: Session = Depends(get_db),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get top performing projects based on revenue.
    """
    return analytics_service.get_top_projects(db, limit)
