import io
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "entity,csv_content,expected_status",
    [
        (
            "employees",
            "name,department_id,salary,revenue_generated\nTest Employee,1,90000,180000",
            200
        ),
        (
            "projects",
            "name,department_id,cost,revenue\nTest Project,1,50000,150000",
            200
        ),
        (
            "timesheets",
            "employee_id,project_id,hours_worked,date\n1,1,8,2023-10-28",
            200
        ),
        (
            "invalid",
            "test,data\n1,2",
            400
        ),
    ]
)
def test_upload_csv(entity, csv_content, expected_status, client, department_head_token_headers):
    """Test uploading CSV files for different entities"""
    # Create a test CSV file
    file = io.BytesIO(csv_content.encode())
    file.name = f"test_{entity}.csv"
    
    response = client.post(
        f"/api/v1/upload/{entity}",
        files={"file": (file.name, file, "text/csv")},
        headers=department_head_token_headers
    )
    assert response.status_code == expected_status
    
    if expected_status == 200:
        data = response.json()
        assert "message" in data
        assert "imported" in data
        assert "failed" in data


def test_upload_non_csv_file(client, department_head_token_headers):
    """Test uploading a non-CSV file"""
    # Create a test text file
    file = io.BytesIO(b"This is not a CSV file")
    file.name = "test.txt"
    
    response = client.post(
        "/api/v1/upload/employees",
        files={"file": (file.name, file, "text/plain")},
        headers=department_head_token_headers
    )
    assert response.status_code == 400
    assert "detail" in response.json()


@patch("app.services.upload_service.import_employees")
def test_upload_employees_csv_with_mock(mock_import, client, department_head_token_headers):
    """Test employee CSV upload with mocked service"""
    # Mock the import service response
    mock_import.return_value = {
        "success": True,
        "errors": [],
        "imported": 5,
        "failed": 0
    }
    
    # Create a test CSV file
    csv_content = "name,department_id,salary,revenue_generated\n"
    csv_content += "Employee 1,1,90000,180000\n"
    csv_content += "Employee 2,1,95000,190000\n"
    csv_content += "Employee 3,2,85000,170000\n"
    csv_content += "Employee 4,2,80000,160000\n"
    csv_content += "Employee 5,1,100000,200000"
    
    file = io.BytesIO(csv_content.encode())
    file.name = "employees.csv"
    
    response = client.post(
        "/api/v1/upload/employees",
        files={"file": (file.name, file, "text/csv")},
        headers=department_head_token_headers
    )
    assert response.status_code == 200
    
    # Verify mock was called
    mock_import.assert_called_once()
    
    # Check response
    data = response.json()
    assert data["message"] == "Import successful"
    assert data["imported"] == 5
    assert data["failed"] == 0


@patch("app.services.upload_service.import_employees")
def test_upload_employees_csv_with_errors(mock_import, client, department_head_token_headers):
    """Test employee CSV upload with validation errors"""
    # Mock the import service response with errors
    mock_import.return_value = {
        "success": False,
        "errors": ["salary must be positive", "department_id must be numeric"],
        "imported": 0,
        "failed": 3
    }
    
    # Create a test CSV file with errors
    csv_content = "name,department_id,salary,revenue_generated\n"
    csv_content += "Employee 1,invalid,90000,180000\n"
    csv_content += "Employee 2,1,-95000,190000\n"
    csv_content += "Employee 3,,85000,170000"
    
    file = io.BytesIO(csv_content.encode())
    file.name = "employees_with_errors.csv"
    
    response = client.post(
        "/api/v1/upload/employees",
        files={"file": (file.name, file, "text/csv")},
        headers=department_head_token_headers
    )
    assert response.status_code == 400
    
    # Verify mock was called
    mock_import.assert_called_once()
    
    # Check response
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "errors" in data["detail"]
    assert len(data["detail"]["errors"]) == 2
