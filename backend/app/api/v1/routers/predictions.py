from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies.auth import get_analyst_permission
from app.db.session import get_db
from app.models.user import User
from app.models.department import Department
from app.services import prediction_service

router = APIRouter()


@router.get("/department/{department_id}")
def predict_department_performance(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    current_user: User = Depends(get_analyst_permission),
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Predict next month's ROI and cost trend for a department.
    
    Returns:
    - Predicted ROI and cost values
    - Trend percentages compared to current values
    - Confidence scores for predictions
    - AI-generated recommendations
    """
    # Check if department exists
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    # Get predictions
    result = prediction_service.predict_department_performance(db, department_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"],
        )
    
    # Schedule model retraining in the background
    background_tasks.add_task(prediction_service.train_department_model, db, department_id)
    
    return result


@router.post("/department/{department_id}/train")
def train_department_model(
    *,
    db: Session = Depends(get_db),
    department_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Any:
    """
    Manually trigger training of prediction models for a department.
    """
    # Check if department exists
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    # Train models
    result = prediction_service.train_department_model(db, department_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"],
        )
    
    return {
        "message": "Department prediction models trained successfully",
        "department_id": department_id,
        "department_name": department.name,
        "roi_model_metrics": result["roi_model_metrics"],
        "cost_model_metrics": result["cost_model_metrics"],
    }
