from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.models.project import Project
from app.models.timesheet import Timesheet


def calculate_employee_roi(salary: float, revenue_generated: float) -> float:
    """Calculate employee ROI: (revenue_generated - salary) / salary"""
    if salary <= 0:
        return 0.0
    return (revenue_generated - salary) / salary


def calculate_department_roi(total_revenue: float, total_cost: float) -> float:
    """Calculate department ROI: (total_revenue - total_cost) / total_cost"""
    if total_cost <= 0:
        return 0.0
    return (total_revenue - total_cost) / total_cost


def calculate_productivity_index(total_revenue: float, total_hours: float) -> float:
    """Calculate productivity index: total_revenue / total_hours_worked"""
    if total_hours <= 0:
        return 0.0
    return total_revenue / total_hours


def get_department_analytics(db: Session, department_id: int) -> Dict[str, Any]:
    """Get analytics for a specific department."""
    # Get department
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        return {}
    
    # Get employees in department
    employees = db.query(Employee).filter(Employee.department_id == department_id).all()
    employee_count = len(employees)
    
    # Calculate total salary cost
    total_salary = db.query(func.sum(Employee.salary)).filter(
        Employee.department_id == department_id
    ).scalar() or 0.0
    
    # Calculate total revenue generated
    total_revenue = db.query(func.sum(Employee.revenue_generated)).filter(
        Employee.department_id == department_id
    ).scalar() or 0.0
    
    # Get projects in department
    projects = db.query(Project).filter(Project.department_id == department_id).all()
    project_count = len(projects)
    
    # Calculate total project cost and revenue
    total_project_cost = db.query(func.sum(Project.cost)).filter(
        Project.department_id == department_id
    ).scalar() or 0.0
    
    total_project_revenue = db.query(func.sum(Project.revenue)).filter(
        Project.department_id == department_id
    ).scalar() or 0.0
    
    # Calculate profit and profit margin
    total_department_revenue = total_revenue + total_project_revenue
    total_department_cost = total_salary + total_project_cost
    profit = total_department_revenue - total_department_cost
    profit_margin = (profit / total_department_revenue) * 100 if total_department_revenue > 0 else 0
    
    # Calculate budget utilization
    budget_utilization = (total_department_cost / department.budget) * 100 if department.budget > 0 else 0
    
    # Calculate ROI
    department_roi = calculate_department_roi(total_department_revenue, total_department_cost)
    
    # Calculate productivity index
    total_hours = db.query(func.sum(Timesheet.hours_worked)).join(Employee).filter(
        Employee.department_id == department_id
    ).scalar() or 0.0
    
    productivity_index = calculate_productivity_index(total_department_revenue, total_hours)
    
    # Generate alerts
    alerts = []
    if department_roi < 0:
        alerts.append("Department is operating at a loss")
    if budget_utilization > 90:
        alerts.append("Department is approaching budget limit")
    if productivity_index < 50 and total_hours > 0:
        alerts.append("Low productivity detected")
    
    return {
        "department_id": department.id,
        "department_name": department.name,
        "budget": department.budget,
        "employee_count": employee_count,
        "project_count": project_count,
        "total_salary_cost": total_salary,
        "total_project_cost": total_project_cost,
        "total_revenue": total_department_revenue,
        "profit": profit,
        "profit_margin": profit_margin,
        "budget_utilization": budget_utilization,
        "roi": department_roi,
        "productivity_index": productivity_index,
        "total_hours": total_hours,
        "alerts": alerts
    }


def get_project_analytics(db: Session, project_id: int) -> Dict:
    """Get analytics for a specific project."""
    # Get project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return {}
    
    # Get department
    department = db.query(Department).filter(Department.id == project.department_id).first()
    
    # Get timesheets for project
    timesheets = db.query(Timesheet).filter(Timesheet.project_id == project_id).all()
    
    # Calculate total hours worked
    total_hours = db.query(func.sum(Timesheet.hours_worked)).filter(
        Timesheet.project_id == project_id
    ).scalar() or 0.0
    
    # Get unique employees who worked on the project
    unique_employees = db.query(Employee).join(Timesheet).filter(
        Timesheet.project_id == project_id
    ).distinct().all()
    
    employee_count = len(unique_employees)
    
    # Calculate average hourly cost
    total_employee_cost = 0.0
    for employee in unique_employees:
        employee_hours = db.query(func.sum(Timesheet.hours_worked)).filter(
            Timesheet.project_id == project_id,
            Timesheet.employee_id == employee.id
        ).scalar() or 0.0
        
        # Assuming 160 working hours per month
        hourly_rate = employee.salary / 160
        total_employee_cost += hourly_rate * employee_hours
    
    # Calculate profit and profit margin
    total_cost = project.cost + total_employee_cost
    profit = project.revenue - total_cost
    profit_margin = (profit / project.revenue) * 100 if project.revenue > 0 else 0
    
    return {
        "project_id": project.id,
        "project_name": project.name,
        "department_id": project.department_id,
        "department_name": department.name if department else "",
        "cost": project.cost,
        "labor_cost": total_employee_cost,
        "total_cost": total_cost,
        "revenue": project.revenue,
        "profit": profit,
        "profit_margin": profit_margin,
        "total_hours": total_hours,
        "employee_count": employee_count
    }


def get_employee_analytics(db: Session, employee_id: int) -> Dict[str, Any]:
    """Get analytics for a specific employee."""
    # Get employee
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return {}
    
    # Get department
    department = db.query(Department).filter(Department.id == employee.department_id).first()
    
    # Get timesheets for employee
    timesheets = db.query(Timesheet).filter(Timesheet.employee_id == employee_id).all()
    
    # Calculate total hours worked
    total_hours = db.query(func.sum(Timesheet.hours_worked)).filter(
        Timesheet.employee_id == employee_id
    ).scalar() or 0.0
    
    # Get unique projects the employee worked on
    unique_projects = db.query(Project).join(Timesheet).filter(
        Timesheet.employee_id == employee_id
    ).distinct().all()
    
    project_count = len(unique_projects)
    
    # Calculate productivity metrics
    # Assuming 160 working hours per month
    hourly_rate = employee.salary / 160
    cost_per_hour = hourly_rate
    revenue_per_hour = employee.revenue_generated / total_hours if total_hours > 0 else 0
    profit_per_hour = revenue_per_hour - cost_per_hour
    
    # Calculate ROI
    employee_roi = calculate_employee_roi(employee.salary, employee.revenue_generated)
    
    # Calculate productivity index
    productivity_index = calculate_productivity_index(employee.revenue_generated, total_hours)
    
    # Calculate utilization (hours logged vs. expected hours)
    # Assuming 8 hours per day, 5 days per week
    current_date = datetime.now().date()
    start_of_month = date(current_date.year, current_date.month, 1)
    days_in_month = (date(current_date.year, current_date.month + 1, 1) - timedelta(days=1)).day
    
    # Count working days (excluding weekends)
    working_days = 0
    for day in range(1, days_in_month + 1):
        current_day = date(current_date.year, current_date.month, day)
        if current_day.weekday() < 5:  # 0-4 are Monday to Friday
            working_days += 1
    
    expected_hours = working_days * 8
    
    # Calculate hours logged this month
    hours_this_month = db.query(func.sum(Timesheet.hours_worked)).filter(
        Timesheet.employee_id == employee_id,
        Timesheet.date >= start_of_month
    ).scalar() or 0.0
    
    utilization_rate = (hours_this_month / expected_hours) * 100 if expected_hours > 0 else 0
    
    # Generate alerts
    alerts = []
    if employee_roi < 0:
        alerts.append("Employee is operating at a loss")
    if utilization_rate < 70:
        alerts.append("Low utilization rate")
    if productivity_index < 50 and total_hours > 0:
        alerts.append("Low productivity detected")
    
    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        "department_id": employee.department_id,
        "department_name": department.name if department else "",
        "salary": employee.salary,
        "revenue_generated": employee.revenue_generated,
        "profit": employee.revenue_generated - employee.salary,
        "total_hours": total_hours,
        "project_count": project_count,
        "cost_per_hour": cost_per_hour,
        "revenue_per_hour": revenue_per_hour,
        "profit_per_hour": profit_per_hour,
        "utilization_rate": utilization_rate,
        "roi": employee_roi,
        "productivity_index": productivity_index,
        "alerts": alerts
    }


def get_company_analytics(db: Session) -> Dict[str, Any]:
    """Get overall company analytics."""
    # Get counts
    department_count = db.query(func.count(Department.id)).scalar() or 0
    employee_count = db.query(func.count(Employee.id)).scalar() or 0
    project_count = db.query(func.count(Project.id)).scalar() or 0
    
    # Calculate financial metrics
    total_salary = db.query(func.sum(Employee.salary)).scalar() or 0.0
    total_project_cost = db.query(func.sum(Project.cost)).scalar() or 0.0
    total_employee_revenue = db.query(func.sum(Employee.revenue_generated)).scalar() or 0.0
    total_project_revenue = db.query(func.sum(Project.revenue)).scalar() or 0.0
    
    total_cost = total_salary + total_project_cost
    total_revenue = total_employee_revenue + total_project_revenue
    profit = total_revenue - total_cost
    profit_margin = (profit / total_revenue) * 100 if total_revenue > 0 else 0
    
    # Calculate total budget across all departments
    total_budget = db.query(func.sum(Department.budget)).scalar() or 0.0
    budget_utilization = (total_cost / total_budget) * 100 if total_budget > 0 else 0
    
    # Calculate productivity metrics
    total_hours = db.query(func.sum(Timesheet.hours_worked)).scalar() or 0.0
    revenue_per_hour = total_revenue / total_hours if total_hours > 0 else 0
    
    # Calculate ROI
    company_roi = calculate_department_roi(total_revenue, total_cost)
    
    # Calculate productivity index
    productivity_index = calculate_productivity_index(total_revenue, total_hours)
    
    # Generate alerts
    alerts = []
    if company_roi < 0:
        alerts.append("Company is operating at a loss")
    if budget_utilization > 90:
        alerts.append("Company is approaching budget limit")
    if productivity_index < 50 and total_hours > 0:
        alerts.append("Low overall productivity detected")
    
    return {
        "department_count": department_count,
        "employee_count": employee_count,
        "project_count": project_count,
        "total_salary": total_salary,
        "total_project_cost": total_project_cost,
        "total_cost": total_cost,
        "total_employee_revenue": total_employee_revenue,
        "total_project_revenue": total_project_revenue,
        "total_revenue": total_revenue,
        "profit": profit,
        "profit_margin": profit_margin,
        "total_budget": total_budget,
        "budget_utilization": budget_utilization,
        "total_hours": total_hours,
        "revenue_per_hour": revenue_per_hour,
        "roi": company_roi,
        "productivity_index": productivity_index,
        "alerts": alerts
    }


def get_top_performers(db: Session, limit: int = 5) -> List[Dict]:
    """Get top performing employees based on revenue generated."""
    top_employees = db.query(Employee).order_by(Employee.revenue_generated.desc()).limit(limit).all()
    
    result = []
    for employee in top_employees:
        department = db.query(Department).filter(Department.id == employee.department_id).first()
        
        # Calculate profit
        profit = employee.revenue_generated - employee.salary
        profit_margin = (profit / employee.revenue_generated) * 100 if employee.revenue_generated > 0 else 0
        
        result.append({
            "employee_id": employee.id,
            "employee_name": employee.name,
            "department_id": employee.department_id,
            "department_name": department.name if department else "",
            "revenue_generated": employee.revenue_generated,
            "salary": employee.salary,
            "profit": profit,
            "profit_margin": profit_margin
        })
    
    return result


def get_top_projects(db: Session, limit: int = 5) -> List[Dict]:
    """Get top performing projects based on revenue."""
    top_projects = db.query(Project).order_by(Project.revenue.desc()).limit(limit).all()
    
    result = []
    for project in top_projects:
        department = db.query(Department).filter(Department.id == project.department_id).first()
        
        # Calculate profit
        profit = project.revenue - project.cost
        profit_margin = (profit / project.revenue) * 100 if project.revenue > 0 else 0
        
        result.append({
            "project_id": project.id,
            "project_name": project.name,
            "department_id": project.department_id,
            "department_name": department.name if department else "",
            "revenue": project.revenue,
            "cost": project.cost,
            "profit": profit,
            "profit_margin": profit_margin
        })
    
    return result
