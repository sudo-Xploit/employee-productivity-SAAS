from typing import Any, Dict

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_department_head_permission
from app.db.session import get_db
from app.models.user import User
from app.services import upload_service

router = APIRouter()


@router.post("/{entity}", response_model=Dict[str, Any])
async def upload_csv(
    *,
    entity: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_department_head_permission),
) -> Any:
    """
    Upload a CSV file to import data.
    
    Supported entities:
    - employees
    - projects
    - timesheets
    """
    # Check file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported",
        )
    
    # Read file content
    file_content = await file.read()
    
    # Process based on entity type
    if entity == "employees":
        result = upload_service.import_employees(db, file_content)
    elif entity == "projects":
        result = upload_service.import_projects(db, file_content)
    elif entity == "timesheets":
        result = upload_service.import_timesheets(db, file_content)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entity '{entity}' not supported. Use 'employees', 'projects', or 'timesheets'.",
        )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Import failed",
                "errors": result["errors"]
            },
        )
    
    return {
        "message": "Import successful",
        "imported": result["imported"],
        "failed": result["failed"]
    }
