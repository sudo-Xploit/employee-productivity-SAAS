import os
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.models.project import Project
from app.models.timesheet import Timesheet


# Path to save trained models
MODEL_DIR = os.path.join(os.getcwd(), "models")
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)


def generate_historical_data(db: Session, department_id: int, months: int = 12) -> pd.DataFrame:
    """
    Generate or retrieve historical data for a department.
    In a real-world scenario, this would pull actual historical data.
    For this implementation, we'll simulate historical data based on current values.
    """
    # Get current department data
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        return pd.DataFrame()
    
    # Get employees in department
    employees = db.query(Employee).filter(Employee.department_id == department_id).all()
    
    # Get projects in department
    projects = db.query(Project).filter(Project.department_id == department_id).all()
    
    # Calculate current metrics
    current_salary_cost = sum(emp.salary for emp in employees)
    current_revenue = sum(emp.revenue_generated for emp in employees)
    current_project_cost = sum(proj.cost for proj in projects)
    current_project_revenue = sum(proj.revenue for proj in projects)
    
    total_cost = current_salary_cost + current_project_cost
    total_revenue = current_revenue + current_project_revenue
    
    # Current ROI
    current_roi = (total_revenue - total_cost) / total_cost if total_cost > 0 else 0
    
    # Generate historical data with some random variations
    np.random.seed(42)  # For reproducibility
    
    # Create date range for historical data
    end_date = datetime.now().date().replace(day=1)  # First day of current month
    start_date = end_date - timedelta(days=30 * months)
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')  # Monthly start
    
    # Create dataframe with historical data
    data = []
    
    for i, date in enumerate(date_range):
        # Add some trend and seasonality
        trend_factor = 1 + (i / len(date_range)) * 0.2  # Gradual increase over time
        seasonal_factor = 1 + 0.1 * np.sin(i / 6 * np.pi)  # Seasonal cycle every 6 months
        random_factor = np.random.normal(1, 0.05)  # Random noise
        
        # Calculate metrics with factors
        month_salary = current_salary_cost * trend_factor * seasonal_factor * random_factor
        month_revenue = current_revenue * trend_factor * seasonal_factor * random_factor * np.random.normal(1, 0.1)
        month_project_cost = current_project_cost * trend_factor * seasonal_factor * random_factor
        month_project_revenue = current_project_revenue * trend_factor * seasonal_factor * random_factor * np.random.normal(1, 0.1)
        
        month_total_cost = month_salary + month_project_cost
        month_total_revenue = month_revenue + month_project_revenue
        month_roi = (month_total_revenue - month_total_cost) / month_total_cost if month_total_cost > 0 else 0
        
        # Add to data
        data.append({
            'date': date,
            'month': date.month,
            'year': date.year,
            'salary_cost': month_salary,
            'project_cost': month_project_cost,
            'total_cost': month_total_cost,
            'revenue': month_total_revenue,
            'roi': month_roi,
            'employee_count': len(employees) + np.random.randint(-1, 2),  # Slight variation in employee count
            'project_count': len(projects) + np.random.randint(-1, 2),  # Slight variation in project count
        })
    
    return pd.DataFrame(data)


def train_department_model(db: Session, department_id: int) -> Dict[str, Any]:
    """
    Train a machine learning model to predict department ROI and cost trends.
    """
    # Get historical data
    historical_data = generate_historical_data(db, department_id)
    
    if historical_data.empty:
        return {
            "success": False,
            "error": "No data available for department"
        }
    
    # Prepare features and targets
    features = historical_data[['month', 'salary_cost', 'project_cost', 'employee_count', 'project_count']]
    roi_target = historical_data['roi']
    cost_target = historical_data['total_cost']
    
    # Split data
    X_train, X_test, y_roi_train, y_roi_test = train_test_split(
        features, roi_target, test_size=0.2, random_state=42
    )
    _, _, y_cost_train, y_cost_test = train_test_split(
        features, cost_target, test_size=0.2, random_state=42
    )
    
    # Train ROI model
    roi_model = RandomForestRegressor(n_estimators=100, random_state=42)
    roi_model.fit(X_train, y_roi_train)
    
    # Train cost model
    cost_model = RandomForestRegressor(n_estimators=100, random_state=42)
    cost_model.fit(X_train, y_cost_train)
    
    # Evaluate models
    roi_predictions = roi_model.predict(X_test)
    roi_mse = mean_squared_error(y_roi_test, roi_predictions)
    roi_r2 = r2_score(y_roi_test, roi_predictions)
    
    cost_predictions = cost_model.predict(X_test)
    cost_mse = mean_squared_error(y_cost_test, cost_predictions)
    cost_r2 = r2_score(y_cost_test, cost_predictions)
    
    # Save models
    roi_model_path = os.path.join(MODEL_DIR, f"department_{department_id}_roi_model.joblib")
    cost_model_path = os.path.join(MODEL_DIR, f"department_{department_id}_cost_model.joblib")
    
    joblib.dump(roi_model, roi_model_path)
    joblib.dump(cost_model, cost_model_path)
    
    return {
        "success": True,
        "department_id": department_id,
        "roi_model_metrics": {
            "mse": roi_mse,
            "r2": roi_r2
        },
        "cost_model_metrics": {
            "mse": cost_mse,
            "r2": cost_r2
        },
        "roi_model_path": roi_model_path,
        "cost_model_path": cost_model_path
    }


def predict_department_performance(db: Session, department_id: int) -> Dict[str, Any]:
    """
    Predict next month's ROI and cost trend for a department.
    """
    # Check if models exist, if not, train them
    roi_model_path = os.path.join(MODEL_DIR, f"department_{department_id}_roi_model.joblib")
    cost_model_path = os.path.join(MODEL_DIR, f"department_{department_id}_cost_model.joblib")
    
    if not os.path.exists(roi_model_path) or not os.path.exists(cost_model_path):
        training_result = train_department_model(db, department_id)
        if not training_result["success"]:
            return {
                "success": False,
                "error": training_result["error"]
            }
    
    # Load models
    roi_model = joblib.load(roi_model_path)
    cost_model = joblib.load(cost_model_path)
    
    # Get current department data
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        return {
            "success": False,
            "error": "Department not found"
        }
    
    # Get employees in department
    employees = db.query(Employee).filter(Employee.department_id == department_id).all()
    
    # Get projects in department
    projects = db.query(Project).filter(Project.department_id == department_id).all()
    
    # Calculate current metrics
    current_salary_cost = sum(emp.salary for emp in employees)
    current_project_cost = sum(proj.cost for proj in projects)
    
    # Prepare prediction input
    next_month = (datetime.now().month % 12) + 1  # Next month number
    prediction_input = np.array([[
        next_month,
        current_salary_cost,
        current_project_cost,
        len(employees),
        len(projects)
    ]])
    
    # Make predictions
    roi_prediction = roi_model.predict(prediction_input)[0]
    cost_prediction = cost_model.predict(prediction_input)[0]
    
    # Calculate confidence scores (using feature importance as a proxy)
    roi_feature_importance = roi_model.feature_importances_
    cost_feature_importance = cost_model.feature_importances_
    
    # Higher importance means more confident prediction
    roi_confidence = min(0.95, 0.5 + sum(roi_feature_importance) / 2)
    cost_confidence = min(0.95, 0.5 + sum(cost_feature_importance) / 2)
    
    # Get current values for comparison
    historical_data = generate_historical_data(db, department_id, months=1)
    current_roi = historical_data['roi'].iloc[-1] if not historical_data.empty else 0
    current_cost = historical_data['total_cost'].iloc[-1] if not historical_data.empty else 0
    
    # Calculate trends
    roi_trend = ((roi_prediction - current_roi) / current_roi) * 100 if current_roi > 0 else 0
    cost_trend = ((cost_prediction - current_cost) / current_cost) * 100 if current_cost > 0 else 0
    
    return {
        "success": True,
        "department_id": department_id,
        "department_name": department.name,
        "prediction_date": datetime.now().strftime("%Y-%m-%d"),
        "next_month": next_month,
        "current_roi": current_roi,
        "predicted_roi": roi_prediction,
        "roi_trend_percent": roi_trend,
        "roi_confidence": roi_confidence,
        "current_cost": current_cost,
        "predicted_cost": cost_prediction,
        "cost_trend_percent": cost_trend,
        "cost_confidence": cost_confidence,
        "recommendations": generate_recommendations(roi_trend, cost_trend)
    }


def generate_recommendations(roi_trend: float, cost_trend: float) -> List[str]:
    """
    Generate recommendations based on predicted trends.
    """
    recommendations = []
    
    if roi_trend > 5:
        recommendations.append("ROI is projected to increase significantly. Consider expanding successful projects.")
    elif roi_trend < -5:
        recommendations.append("ROI is projected to decrease. Review project performance and consider cost-cutting measures.")
    else:
        recommendations.append("ROI is projected to remain stable. Maintain current strategy.")
    
    if cost_trend > 10:
        recommendations.append("Costs are projected to increase significantly. Review budget allocations and identify areas for optimization.")
    elif cost_trend < -5:
        recommendations.append("Costs are projected to decrease. Ensure this doesn't impact quality or employee satisfaction.")
    else:
        recommendations.append("Costs are projected to remain stable. Continue monitoring for any changes.")
    
    return recommendations
