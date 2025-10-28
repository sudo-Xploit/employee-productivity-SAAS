from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.session import get_async_db
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee
from app.api.v1.dependencies.auth import get_analyst_permission
from app.services import analytics_service
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/company", summary="Get company-wide analytics")
async def get_company_analytics(
    db: Session = Depends(get_async_db),
    current_user: User = Depends(get_analyst_permission),
) -> Dict[str, Any]:
    """
    Get company-wide analytics including financial metrics, productivity indices, and alerts.
    
    Returns:
        Dict[str, Any]: Company analytics data
    """
    logger.info("Fetching company analytics", extra={"user_id": current_user.id})
    try:
        result = analytics_service.get_company_analytics(db)
        return result
    except Exception as e:
        logger.error(f"Error fetching company analytics: {str(e)}", extra={"user_id": current_user.id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching company analytics: {str(e)}",
        )


@router.get("/departments/{department_id}", summary="Get department analytics")
async def get_department_analytics(
    *,
    db: Session = Depends(get_async_db),
    department_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Dict[str, Any]:
    """
    Get analytics for a specific department including ROI, productivity indices, and alerts.
    
    Parameters:
        department_id: ID of the department to analyze
        
    Returns:
        Dict[str, Any]: Department analytics data
    """
    logger.info(f"Fetching department analytics for department_id={department_id}", 
                extra={"user_id": current_user.id, "department_id": department_id})
    
    # Check if department exists
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        logger.warning(f"Department not found: department_id={department_id}", 
                      extra={"user_id": current_user.id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    try:
        result = analytics_service.get_department_analytics(db, department_id)
        return result
    except Exception as e:
        logger.error(f"Error fetching department analytics: {str(e)}", 
                    extra={"user_id": current_user.id, "department_id": department_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching department analytics: {str(e)}",
        )


@router.get("/employees/{employee_id}", summary="Get employee analytics")
async def get_employee_analytics(
    *,
    db: Session = Depends(get_async_db),
    employee_id: int,
    current_user: User = Depends(get_analyst_permission),
) -> Dict[str, Any]:
    """
    Get analytics for a specific employee including ROI, productivity indices, and alerts.
    
    Parameters:
        employee_id: ID of the employee to analyze
        
    Returns:
        Dict[str, Any]: Employee analytics data
    """
    logger.info(f"Fetching employee analytics for employee_id={employee_id}", 
                extra={"user_id": current_user.id, "employee_id": employee_id})
    
    # Check if employee exists
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        logger.warning(f"Employee not found: employee_id={employee_id}", 
                      extra={"user_id": current_user.id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    
    try:
        result = analytics_service.get_employee_analytics(db, employee_id)
        return result
    except Exception as e:
        logger.error(f"Error fetching employee analytics: {str(e)}", 
                    extra={"user_id": current_user.id, "employee_id": employee_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee analytics: {str(e)}",
        )


@router.get("/top-performers", summary="Get top performing employees")
async def get_top_performers(
    *,
    db: Session = Depends(get_async_db),
    limit: int = 5,
    current_user: User = Depends(get_analyst_permission),
) -> List[Dict[str, Any]]:
    """
    Get a list of top performing employees based on revenue generated.
    
    Parameters:
        limit: Maximum number of employees to return (default: 5)
        
    Returns:
        List[Dict[str, Any]]: List of top performing employees
    """
    logger.info(f"Fetching top performers with limit={limit}", 
                extra={"user_id": current_user.id})
    
    try:
        result = analytics_service.get_top_performers(db, limit)
        return result
    except Exception as e:
        logger.error(f"Error fetching top performers: {str(e)}", 
                    extra={"user_id": current_user.id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching top performers: {str(e)}",
        )
