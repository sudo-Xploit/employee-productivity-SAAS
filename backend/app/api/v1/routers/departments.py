from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_analyst_permission, get_department_head_permission
from app.api.v1.schemas.department import Department, DepartmentCreate, DepartmentUpdate
from app.db.session import get_db
from app.models.user import User
from app.services import department_service, employee_service

router = APIRouter()


@router.get("/", response_model=List[Department])
def read_departments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Retrieve departments.
    """
    departments = department_service.get_multi(db, skip=skip, limit=limit)
    return departments


@router.post("/", response_model=Department, status_code=status.HTTP_201_CREATED)
def create_department(
    *,
    db: Session = Depends(get_db),
    department_in: DepartmentCreate,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Create new department.
    """
    department = department_service.get_by_name(db, name=department_in.name)
    if department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department with this name already exists",
        )
    department = department_service.create(db, obj_in=department_in.model_dump())
    return department


@router.get("/{department_id}", response_model=Department)
def read_department(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get department by ID.
    """
    department = department_service.get(db, department_id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    return department


@router.put("/{department_id}", response_model=Department)
def update_department(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    department_in: DepartmentUpdate,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Update a department.
    """
    department = department_service.get(db, department_id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    if department_in.name and department_in.name != department.name:
        existing_department = department_service.get_by_name(db, name=department_in.name)
        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department with this name already exists",
            )
    department = department_service.update(db, db_obj=department, obj_in=department_in.model_dump(exclude_unset=True))
    return department


@router.delete("/{department_id}", response_model=Department)
def delete_department(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Delete a department.
    """
    department = department_service.get(db, department_id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    # Check if department has employees
    employees = employee_service.get_by_department(db, department_id=department_id)
    if employees:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete department with employees. Reassign employees first.",
        )
    
    department = department_service.remove(db, department_id=department_id)
    return department


@router.get("/{department_id}/employees", response_model=List[Any])
def read_department_employees(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get employees for a specific department.
    """
    department = department_service.get(db, department_id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    employees = employee_service.get_by_department(
        db, department_id=department_id, skip=skip, limit=limit
    )
    return employees
