from datetime import date
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_analyst_permission, get_department_head_permission
from app.db.session import get_db
from app.models.user import User
from app.services import employee_service, project_service, timesheet_service

router = APIRouter()


@router.get("/")
def read_timesheets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Retrieve timesheets with optional date filtering.
    """
    if start_date and end_date:
        timesheets = timesheet_service.get_by_date_range(
            db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
        )
    else:
        timesheets = timesheet_service.get_multi(db, skip=skip, limit=limit)
    return timesheets


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_timesheet(
    *,
    db: Session = Depends(get_db),
    timesheet_data: Dict[str, Any],
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Create new timesheet entry.
    """
    # Check if employee exists
    employee = employee_service.get(db, employee_id=timesheet_data.get("employee_id"))
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    
    # Check if project exists
    project = project_service.get(db, project_id=timesheet_data.get("project_id"))
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    timesheet = timesheet_service.create(db, obj_in=timesheet_data)
    return timesheet


@router.get("/{timesheet_id}")
def read_timesheet(
    *,
    db: Session = Depends(get_db),
    timesheet_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get timesheet by ID.
    """
    timesheet = timesheet_service.get(db, timesheet_id=timesheet_id)
    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timesheet not found",
        )
    return timesheet


@router.put("/{timesheet_id}")
def update_timesheet(
    *,
    db: Session = Depends(get_db),
    timesheet_id: int,
    timesheet_data: Dict[str, Any],
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Update a timesheet entry.
    """
    timesheet = timesheet_service.get(db, timesheet_id=timesheet_id)
    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timesheet not found",
        )
    
    # If employee_id is being updated, check if the new employee exists
    if "employee_id" in timesheet_data and timesheet_data["employee_id"] != timesheet.employee_id:
        employee = employee_service.get(db, employee_id=timesheet_data["employee_id"])
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )
    
    # If project_id is being updated, check if the new project exists
    if "project_id" in timesheet_data and timesheet_data["project_id"] != timesheet.project_id:
        project = project_service.get(db, project_id=timesheet_data["project_id"])
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
    
    timesheet = timesheet_service.update(db, db_obj=timesheet, obj_in=timesheet_data)
    return timesheet


@router.delete("/{timesheet_id}")
def delete_timesheet(
    *,
    db: Session = Depends(get_db),
    timesheet_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Delete a timesheet entry.
    """
    timesheet = timesheet_service.get(db, timesheet_id=timesheet_id)
    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timesheet not found",
        )
    timesheet = timesheet_service.remove(db, timesheet_id=timesheet_id)
    return timesheet


@router.get("/employee/{employee_id}")
def read_employee_timesheets(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get timesheets for a specific employee.
    """
    employee = employee_service.get(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    timesheets = timesheet_service.get_by_employee(
        db, employee_id=employee_id, skip=skip, limit=limit
    )
    return timesheets


@router.get("/project/{project_id}")
def read_project_timesheets(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get timesheets for a specific project.
    """
    project = project_service.get(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    timesheets = timesheet_service.get_by_project(
        db, project_id=project_id, skip=skip, limit=limit
    )
    return timesheets
