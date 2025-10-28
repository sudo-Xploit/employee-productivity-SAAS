from typing import Any, Dict

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.post("/{entity}")
async def upload_csv(
    *,
    entity: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
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
        return {
            "message": "Employee CSV upload simulation",
            "entity": entity,
            "filename": file.filename,
            "size": len(file_content)
        }
    elif entity == "projects":
        return {
            "message": "Project CSV upload simulation",
            "entity": entity,
            "filename": file.filename,
            "size": len(file_content)
        }
    elif entity == "timesheets":
        return {
            "message": "Timesheet CSV upload simulation",
            "entity": entity,
            "filename": file.filename,
            "size": len(file_content)
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entity '{entity}' not supported. Use 'employees', 'projects', or 'timesheets'.",
        )
