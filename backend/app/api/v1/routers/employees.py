from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_analyst_permission, get_department_head_permission
from app.api.v1.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate, EmployeeWithDetails
from app.db.session import get_db
from app.models.user import User
from app.services import employee_service

router = APIRouter()


@router.get("/", response_model=List[Employee])
def read_employees(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Retrieve employees.
    """
    employees = employee_service.get_multi(db, skip=skip, limit=limit)
    return employees


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(
    *,
    db: Session = Depends(get_db),
    employee_in: EmployeeCreate,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Create new employee.
    """
    employee = employee_service.create(db, obj_in=employee_in.model_dump())
    return employee


@router.get("/{employee_id}", response_model=Employee)
def read_employee(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get employee by ID.
    """
    employee = employee_service.get(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    employee_in: EmployeeUpdate,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Update an employee.
    """
    employee = employee_service.get(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    employee = employee_service.update(db, db_obj=employee, obj_in=employee_in.model_dump(exclude_unset=True))
    return employee


@router.delete("/{employee_id}", response_model=Employee)
def delete_employee(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Delete an employee.
    """
    employee = employee_service.get(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    employee = employee_service.remove(db, employee_id=employee_id)
    return employee