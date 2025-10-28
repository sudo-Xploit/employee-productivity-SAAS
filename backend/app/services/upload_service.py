import io
import logging
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.project import Project
from app.models.timesheet import Timesheet
from app.models.department import Department

logger = logging.getLogger(__name__)

class UploadError(Exception):
    """Exception raised for errors in the upload process."""
    pass

def validate_employee_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Validate employee data from CSV."""
    errors = []
    
    # Check required columns
    required_columns = ["name", "department_id", "salary"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, errors
    
    # Check data types
    if not pd.api.types.is_numeric_dtype(df["department_id"]):
        errors.append("department_id must be numeric")
    
    if not pd.api.types.is_numeric_dtype(df["salary"]):
        errors.append("salary must be numeric")
    
    # Check for negative salary
    if (df["salary"] <= 0).any():
        errors.append("salary must be positive")
    
    # Check for empty names
    if df["name"].isna().any() or (df["name"] == "").any():
        errors.append("name cannot be empty")
    
    return len(errors) == 0, errors

def validate_project_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Validate project data from CSV."""
    errors = []
    
    # Check required columns
    required_columns = ["name", "department_id", "cost", "revenue"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, errors
    
    # Check data types
    if not pd.api.types.is_numeric_dtype(df["department_id"]):
        errors.append("department_id must be numeric")
    
    if not pd.api.types.is_numeric_dtype(df["cost"]):
        errors.append("cost must be numeric")
    
    if not pd.api.types.is_numeric_dtype(df["revenue"]):
        errors.append("revenue must be numeric")
    
    # Check for negative values
    if (df["cost"] < 0).any():
        errors.append("cost cannot be negative")
    
    if (df["revenue"] < 0).any():
        errors.append("revenue cannot be negative")
    
    # Check for empty names
    if df["name"].isna().any() or (df["name"] == "").any():
        errors.append("name cannot be empty")
    
    return len(errors) == 0, errors

def validate_timesheet_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Validate timesheet data from CSV."""
    errors = []
    
    # Check required columns
    required_columns = ["employee_id", "project_id", "hours_worked", "date"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, errors
    
    # Check data types
    if not pd.api.types.is_numeric_dtype(df["employee_id"]):
        errors.append("employee_id must be numeric")
    
    if not pd.api.types.is_numeric_dtype(df["project_id"]):
        errors.append("project_id must be numeric")
    
    if not pd.api.types.is_numeric_dtype(df["hours_worked"]):
        errors.append("hours_worked must be numeric")
    
    # Check for valid date format
    try:
        pd.to_datetime(df["date"])
    except:
        errors.append("date must be in a valid date format (YYYY-MM-DD)")
    
    # Check for negative or zero hours
    if (df["hours_worked"] <= 0).any():
        errors.append("hours_worked must be positive")
    
    return len(errors) == 0, errors

def import_employees(db: Session, file_content: bytes) -> Dict[str, Any]:
    """Import employees from CSV file."""
    try:
        # Read CSV
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Validate data
        is_valid, errors = validate_employee_data(df)
        if not is_valid:
            return {
                "success": False,
                "errors": errors,
                "imported": 0,
                "failed": len(df)
            }
        
        # Check if departments exist
        department_ids = df["department_id"].unique()
        existing_departments = db.query(Department.id).filter(Department.id.in_(department_ids)).all()
        existing_department_ids = [d[0] for d in existing_departments]
        
        missing_departments = [id for id in department_ids if id not in existing_department_ids]
        if missing_departments:
            return {
                "success": False,
                "errors": [f"Department IDs not found: {', '.join(map(str, missing_departments))}"],
                "imported": 0,
                "failed": len(df)
            }
        
        # Import data
        imported = 0
        failed = 0
        
        for _, row in df.iterrows():
            try:
                employee = Employee(
                    name=row["name"],
                    department_id=row["department_id"],
                    salary=row["salary"],
                    revenue_generated=row.get("revenue_generated", 0.0)
                )
                db.add(employee)
                imported += 1
            except Exception as e:
                logger.error(f"Error importing employee: {str(e)}")
                failed += 1
        
        db.commit()
        
        return {
            "success": True,
            "errors": [],
            "imported": imported,
            "failed": failed
        }
    
    except Exception as e:
        logger.error(f"Error in import_employees: {str(e)}")
        db.rollback()
        return {
            "success": False,
            "errors": [str(e)],
            "imported": 0,
            "failed": 0
        }

def import_projects(db: Session, file_content: bytes) -> Dict[str, Any]:
    """Import projects from CSV file."""
    try:
        # Read CSV
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Validate data
        is_valid, errors = validate_project_data(df)
        if not is_valid:
            return {
                "success": False,
                "errors": errors,
                "imported": 0,
                "failed": len(df)
            }
        
        # Check if departments exist
        department_ids = df["department_id"].unique()
        existing_departments = db.query(Department.id).filter(Department.id.in_(department_ids)).all()
        existing_department_ids = [d[0] for d in existing_departments]
        
        missing_departments = [id for id in department_ids if id not in existing_department_ids]
        if missing_departments:
            return {
                "success": False,
                "errors": [f"Department IDs not found: {', '.join(map(str, missing_departments))}"],
                "imported": 0,
                "failed": len(df)
            }
        
        # Import data
        imported = 0
        failed = 0
        
        for _, row in df.iterrows():
            try:
                project = Project(
                    name=row["name"],
                    department_id=row["department_id"],
                    cost=row["cost"],
                    revenue=row["revenue"]
                )
                db.add(project)
                imported += 1
            except Exception as e:
                logger.error(f"Error importing project: {str(e)}")
                failed += 1
        
        db.commit()
        
        return {
            "success": True,
            "errors": [],
            "imported": imported,
            "failed": failed
        }
    
    except Exception as e:
        logger.error(f"Error in import_projects: {str(e)}")
        db.rollback()
        return {
            "success": False,
            "errors": [str(e)],
            "imported": 0,
            "failed": 0
        }

def import_timesheets(db: Session, file_content: bytes) -> Dict[str, Any]:
    """Import timesheets from CSV file."""
    try:
        # Read CSV
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Validate data
        is_valid, errors = validate_timesheet_data(df)
        if not is_valid:
            return {
                "success": False,
                "errors": errors,
                "imported": 0,
                "failed": len(df)
            }
        
        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"]).dt.date
        
        # Check if employees exist
        employee_ids = df["employee_id"].unique()
        existing_employees = db.query(Employee.id).filter(Employee.id.in_(employee_ids)).all()
        existing_employee_ids = [e[0] for e in existing_employees]
        
        missing_employees = [id for id in employee_ids if id not in existing_employee_ids]
        if missing_employees:
            return {
                "success": False,
                "errors": [f"Employee IDs not found: {', '.join(map(str, missing_employees))}"],
                "imported": 0,
                "failed": len(df)
            }
        
        # Check if projects exist
        project_ids = df["project_id"].unique()
        existing_projects = db.query(Project.id).filter(Project.id.in_(project_ids)).all()
        existing_project_ids = [p[0] for p in existing_projects]
        
        missing_projects = [id for id in project_ids if id not in existing_project_ids]
        if missing_projects:
            return {
                "success": False,
                "errors": [f"Project IDs not found: {', '.join(map(str, missing_projects))}"],
                "imported": 0,
                "failed": len(df)
            }
        
        # Import data
        imported = 0
        failed = 0
        
        for _, row in df.iterrows():
            try:
                timesheet = Timesheet(
                    employee_id=row["employee_id"],
                    project_id=row["project_id"],
                    hours_worked=row["hours_worked"],
                    date=row["date"]
                )
                db.add(timesheet)
                imported += 1
            except Exception as e:
                logger.error(f"Error importing timesheet: {str(e)}")
                failed += 1
        
        db.commit()
        
        return {
            "success": True,
            "errors": [],
            "imported": imported,
            "failed": failed
        }
    
    except Exception as e:
        logger.error(f"Error in import_timesheets: {str(e)}")
        db.rollback()
        return {
            "success": False,
            "errors": [str(e)],
            "imported": 0,
            "failed": 0
        }
