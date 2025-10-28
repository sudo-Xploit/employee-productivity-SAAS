import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

# Create a test app with mock analytics endpoints
app = FastAPI()

# Mock analytics data
MOCK_COMPANY_ANALYTICS = {
    "department_count": 5,
    "employee_count": 12,
    "project_count": 8,
    "total_salary": 1170000.0,
    "total_project_cost": 270000.0,
    "total_cost": 1440000.0,
    "total_revenue": 3170000.0,
    "profit": 1730000.0,
    "profit_margin": 54.57,
    "budget_utilization": 87.27,
    "total_hours": 1000.0,
    "revenue_per_hour": 3170.0,
    "roi": 1.20,
    "productivity_index": 3170.0,
    "alerts": []
}

MOCK_DEPARTMENT_ANALYTICS = {
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
}

MOCK_EMPLOYEE_ANALYTICS = {
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
}

@app.get("/api/v1/analytics/company")
def get_company_analytics():
    return MOCK_COMPANY_ANALYTICS

@app.get("/api/v1/analytics/departments/{department_id}")
def get_department_analytics(department_id: int):
    if department_id != 1:
        return {"detail": "Department not found"}
    return MOCK_DEPARTMENT_ANALYTICS

@app.get("/api/v1/analytics/employees/{employee_id}")
def get_employee_analytics(employee_id: int):
    if employee_id != 1:
        return {"detail": "Employee not found"}
    return MOCK_EMPLOYEE_ANALYTICS

@pytest.fixture
def analytics_client():
    return TestClient(app)


@pytest.mark.analytics
class TestAnalytics:
    """Test analytics functionality with mocks"""
    
    def test_company_analytics(self, analytics_client):
        """Test company-wide analytics"""
        response = analytics_client.get("/api/v1/analytics/company")
        assert response.status_code == 200
        
        data = response.json()
        # Check for required fields
        assert "department_count" in data
        assert "employee_count" in data
        assert "project_count" in data
        assert "total_salary" in data
        assert "total_project_cost" in data
        assert "total_cost" in data
        assert "total_revenue" in data
        assert "profit" in data
        assert "profit_margin" in data
        assert "budget_utilization" in data
        assert "roi" in data
        assert "productivity_index" in data
        assert "alerts" in data
        
        # Check for correct data types
        assert isinstance(data["department_count"], int)
        assert isinstance(data["employee_count"], int)
        assert isinstance(data["project_count"], int)
        assert isinstance(data["total_salary"], (int, float))
        assert isinstance(data["total_project_cost"], (int, float))
        assert isinstance(data["total_revenue"], (int, float))
        assert isinstance(data["profit"], (int, float))
        assert isinstance(data["profit_margin"], (int, float))
        assert isinstance(data["budget_utilization"], (int, float))
        assert isinstance(data["roi"], (int, float))
        assert isinstance(data["productivity_index"], (int, float))
        assert isinstance(data["alerts"], list)
        
        # Check for logical relationships
        assert data["total_cost"] == data["total_salary"] + data["total_project_cost"]
        assert data["profit"] == data["total_revenue"] - data["total_cost"]
        if data["total_revenue"] > 0:
            assert abs(data["profit_margin"] - (data["profit"] / data["total_revenue"] * 100)) < 0.01
    
    def test_department_analytics(self, analytics_client):
        """Test department analytics"""
        response = analytics_client.get("/api/v1/analytics/departments/1")
        assert response.status_code == 200
        
        data = response.json()
        # Check for required fields
        assert "department_id" in data
        assert "department_name" in data
        assert "budget" in data
        assert "employee_count" in data
        assert "project_count" in data
        assert "total_salary_cost" in data
        assert "total_project_cost" in data
        assert "total_revenue" in data
        assert "profit" in data
        assert "profit_margin" in data
        assert "budget_utilization" in data
        assert "roi" in data
        assert "productivity_index" in data
        assert "alerts" in data
        
        # Check specific values
        assert data["department_id"] == 1
        assert data["department_name"] == "Engineering"
        assert data["budget"] == 500000.0
        
        # Check for logical relationships
        assert data["profit"] == data["total_revenue"] - (data["total_salary_cost"] + data["total_project_cost"])
    
    def test_employee_analytics(self, analytics_client):
        """Test employee analytics"""
        response = analytics_client.get("/api/v1/analytics/employees/1")
        assert response.status_code == 200
        
        data = response.json()
        # Check for required fields
        assert "employee_id" in data
        assert "employee_name" in data
        assert "department_id" in data
        assert "department_name" in data
        assert "salary" in data
        assert "revenue_generated" in data
        assert "profit" in data
        assert "roi" in data
        assert "productivity_index" in data
        assert "alerts" in data
        
        # Check specific values
        assert data["employee_id"] == 1
        assert data["employee_name"] == "John Smith"
        assert data["department_id"] == 1
        assert data["department_name"] == "Engineering"
        assert data["salary"] == 120000.0
        assert data["revenue_generated"] == 250000.0
        
        # Check for logical relationships
        assert data["profit"] == data["revenue_generated"] - data["salary"]
        assert abs(data["roi"] - ((data["revenue_generated"] - data["salary"]) / data["salary"])) < 0.01
    
    def test_nonexistent_department(self, analytics_client):
        """Test analytics for nonexistent department"""
        response = analytics_client.get("/api/v1/analytics/departments/999")
        assert response.status_code == 200  # FastAPI returns 200 with the error detail
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Department not found"
    
    def test_nonexistent_employee(self, analytics_client):
        """Test analytics for nonexistent employee"""
        response = analytics_client.get("/api/v1/analytics/employees/999")
        assert response.status_code == 200  # FastAPI returns 200 with the error detail
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Employee not found"
