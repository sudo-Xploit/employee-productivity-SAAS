from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("/company")
def get_company_analytics(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get overall company analytics.
    """
    # This is a simplified version that returns mock data
    return {
        "department_count": 5,
        "employee_count": 12,
        "project_count": 8,
        "total_salary": 1170000.0,
        "total_project_cost": 270000.0,
        "total_cost": 1440000.0,
        "total_employee_revenue": 2230000.0,
        "total_project_revenue": 940000.0,
        "total_revenue": 3170000.0,
        "profit": 1730000.0,
        "profit_margin": 54.57,
        "total_budget": 1650000.0,
        "budget_utilization": 87.27,
        "total_hours": 1000.0,
        "revenue_per_hour": 3170.0,
        "roi": 1.20,
        "productivity_index": 3170.0,
        "alerts": []
    }


@router.get("/departments/{department_id}")
def get_department_analytics(
    *,
    db: Session = Depends(get_db),
    department_id: int,
) -> Any:
    """
    Get analytics for a specific department.
    """
    # This is a simplified version that returns mock data
    if department_id <= 0 or department_id > 5:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    
    # Mock data for different departments
    department_data = {
        1: {
            "department_id": 1,
            "department_name": "Engineering",
            "budget": 500000.0,
            "employee_count": 3,
            "project_count": 2,
            "total_salary_cost": 325000.0,
            "total_project_cost": 130000.0,
            "total_revenue": 800000.0,
            "profit": 345000.0,
            "profit_margin": 43.13,
            "budget_utilization": 91.0,
            "roi": 0.76,
            "productivity_index": 670.0,
            "total_hours": 1194.0,
            "alerts": []
        },
        2: {
            "department_id": 2,
            "department_name": "Marketing",
            "budget": 300000.0,
            "employee_count": 2,
            "project_count": 2,
            "total_salary_cost": 175000.0,
            "total_project_cost": 65000.0,
            "total_revenue": 570000.0,
            "profit": 330000.0,
            "profit_margin": 57.89,
            "budget_utilization": 80.0,
            "roi": 1.38,
            "productivity_index": 712.5,
            "total_hours": 800.0,
            "alerts": []
        }
    }
    
    # Return data for the requested department or a generic response
    return department_data.get(department_id, {
        "department_id": department_id,
        "department_name": f"Department {department_id}",
        "budget": 300000.0,
        "employee_count": 2,
        "project_count": 2,
        "total_salary_cost": 200000.0,
        "total_project_cost": 50000.0,
        "total_revenue": 400000.0,
        "profit": 150000.0,
        "profit_margin": 37.5,
        "budget_utilization": 83.33,
        "roi": 0.6,
        "productivity_index": 500.0,
        "total_hours": 800.0,
        "alerts": []
    })


@router.get("/employees/{employee_id}")
def get_employee_analytics(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
) -> Any:
    """
    Get analytics for a specific employee.
    """
    # This is a simplified version that returns mock data
    if employee_id <= 0 or employee_id > 12:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    
    # Mock data for different employees
    employee_data = {
        1: {
            "employee_id": 1,
            "employee_name": "John Smith",
            "department_id": 1,
            "department_name": "Engineering",
            "salary": 120000.0,
            "revenue_generated": 250000.0,
            "profit": 130000.0,
            "total_hours": 400.0,
            "project_count": 2,
            "cost_per_hour": 62.5,
            "revenue_per_hour": 625.0,
            "profit_per_hour": 562.5,
            "utilization_rate": 95.0,
            "roi": 1.08,
            "productivity_index": 625.0,
            "alerts": []
        },
        2: {
            "employee_id": 2,
            "employee_name": "Jane Doe",
            "department_id": 1,
            "department_name": "Engineering",
            "salary": 110000.0,
            "revenue_generated": 220000.0,
            "profit": 110000.0,
            "total_hours": 380.0,
            "project_count": 2,
            "cost_per_hour": 57.29,
            "revenue_per_hour": 578.95,
            "profit_per_hour": 521.66,
            "utilization_rate": 90.48,
            "roi": 1.0,
            "productivity_index": 578.95,
            "alerts": []
        }
    }
    
    # Return data for the requested employee or a generic response
    return employee_data.get(employee_id, {
        "employee_id": employee_id,
        "employee_name": f"Employee {employee_id}",
        "department_id": (employee_id % 5) + 1,
        "department_name": f"Department {(employee_id % 5) + 1}",
        "salary": 100000.0,
        "revenue_generated": 200000.0,
        "profit": 100000.0,
        "total_hours": 400.0,
        "project_count": 2,
        "cost_per_hour": 52.08,
        "revenue_per_hour": 500.0,
        "profit_per_hour": 447.92,
        "utilization_rate": 95.0,
        "roi": 1.0,
        "productivity_index": 500.0,
        "alerts": []
    })
