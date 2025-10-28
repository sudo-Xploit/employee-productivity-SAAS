from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_analyst_permission, get_department_head_permission
from app.api.v1.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.db.session import get_db
from app.models.user import User
from app.services import department_service, project_service, timesheet_service

router = APIRouter()


@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Retrieve projects.
    """
    projects = project_service.get_multi(db, skip=skip, limit=limit)
    return projects


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Create new project.
    """
    # Check if department exists
    department = department_service.get(db, department_id=project_in.department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    project = project_service.create(db, obj_in=project_in.model_dump())
    return project


@router.get("/{project_id}", response_model=Project)
def read_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get project by ID.
    """
    project = project_service.get(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.put("/{project_id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Update a project.
    """
    project = project_service.get(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # If department_id is being updated, check if the new department exists
    if project_in.department_id is not None and project_in.department_id != project.department_id:
        department = department_service.get(db, department_id=project_in.department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )
    
    project = project_service.update(db, db_obj=project, obj_in=project_in.model_dump(exclude_unset=True))
    return project


@router.delete("/{project_id}", response_model=Project)
def delete_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Delete a project.
    """
    project = project_service.get(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check if project has timesheets
    # This check would require a timesheet_service.get_by_project function
    # For now, we'll assume the cascade delete will handle this
    
    project = project_service.remove(db, project_id=project_id)
    return project


@router.get("/department/{department_id}", response_model=List[Project])
def read_department_projects(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Get projects for a specific department.
    """
    department = department_service.get(db, department_id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    projects = project_service.get_by_department(
        db, department_id=department_id, skip=skip, limit=limit
    )
    return projects
