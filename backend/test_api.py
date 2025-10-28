import requests
import json
import os
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

# Test user credentials
TEST_USER = {
    "email": "admin@example.com",
    "password": "admin123"
}

def login():
    """Login and get access token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def test_analytics(token):
    """Test analytics endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test company analytics
    response = requests.get(f"{BASE_URL}/analytics/company", headers=headers)
    if response.status_code == 200:
        print("Company analytics: Success")
        data = response.json()
        print(f"  ROI: {data.get('roi', 'N/A')}")
        print(f"  Productivity Index: {data.get('productivity_index', 'N/A')}")
        print(f"  Alerts: {data.get('alerts', [])}")
    else:
        print(f"Company analytics failed: {response.status_code}")
        print(response.text)
    
    # Test department analytics (assuming department ID 1 exists)
    response = requests.get(f"{BASE_URL}/analytics/departments/1", headers=headers)
    if response.status_code == 200:
        print("Department analytics: Success")
        data = response.json()
        print(f"  Department: {data.get('department_name', 'N/A')}")
        print(f"  ROI: {data.get('roi', 'N/A')}")
        print(f"  Alerts: {data.get('alerts', [])}")
    else:
        print(f"Department analytics failed: {response.status_code}")
        print(response.text)
    
    # Test employee analytics (assuming employee ID 1 exists)
    response = requests.get(f"{BASE_URL}/analytics/employees/1", headers=headers)
    if response.status_code == 200:
        print("Employee analytics: Success")
        data = response.json()
        print(f"  Employee: {data.get('employee_name', 'N/A')}")
        print(f"  ROI: {data.get('roi', 'N/A')}")
        print(f"  Alerts: {data.get('alerts', [])}")
    else:
        print(f"Employee analytics failed: {response.status_code}")
        print(response.text)

def test_csv_upload(token):
    """Test CSV upload endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test employee CSV upload
    employee_csv_path = os.path.join("sample_data", "employees.csv")
    if os.path.exists(employee_csv_path):
        with open(employee_csv_path, "rb") as f:
            files = {"file": ("employees.csv", f, "text/csv")}
            response = requests.post(
                f"{BASE_URL}/upload/employees",
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                print("Employee CSV upload: Success")
                print(response.json())
            else:
                print(f"Employee CSV upload failed: {response.status_code}")
                print(response.text)
    else:
        print(f"Employee CSV file not found: {employee_csv_path}")
    
    # Test project CSV upload
    project_csv_path = os.path.join("sample_data", "projects.csv")
    if os.path.exists(project_csv_path):
        with open(project_csv_path, "rb") as f:
            files = {"file": ("projects.csv", f, "text/csv")}
            response = requests.post(
                f"{BASE_URL}/upload/projects",
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                print("Project CSV upload: Success")
                print(response.json())
            else:
                print(f"Project CSV upload failed: {response.status_code}")
                print(response.text)
    else:
        print(f"Project CSV file not found: {project_csv_path}")
    
    # Test timesheet CSV upload
    timesheet_csv_path = os.path.join("sample_data", "timesheets.csv")
    if os.path.exists(timesheet_csv_path):
        with open(timesheet_csv_path, "rb") as f:
            files = {"file": ("timesheets.csv", f, "text/csv")}
            response = requests.post(
                f"{BASE_URL}/upload/timesheets",
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                print("Timesheet CSV upload: Success")
                print(response.json())
            else:
                print(f"Timesheet CSV upload failed: {response.status_code}")
                print(response.text)
    else:
        print(f"Timesheet CSV file not found: {timesheet_csv_path}")

def test_reports(token):
    """Test report generation endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test PDF report generation
    response = requests.get(
        f"{BASE_URL}/reports/generate?report_type=pdf",
        headers=headers
    )
    
    if response.status_code == 200:
        # Save the PDF report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.pdf"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"PDF report generated: {filename}")
    else:
        print(f"PDF report generation failed: {response.status_code}")
        print(response.text)
    
    # Test Excel report generation
    response = requests.get(
        f"{BASE_URL}/reports/generate?report_type=excel",
        headers=headers
    )
    
    if response.status_code == 200:
        # Save the Excel report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.xlsx"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Excel report generated: {filename}")
    else:
        print(f"Excel report generation failed: {response.status_code}")
        print(response.text)

def main():
    """Main test function"""
    print("Starting API tests...")
    
    # Login
    token = login()
    if not token:
        print("Authentication failed. Exiting tests.")
        return
    
    print("\n=== Testing Analytics ===")
    test_analytics(token)
    
    print("\n=== Testing CSV Uploads ===")
    test_csv_upload(token)
    
    print("\n=== Testing Reports ===")
    test_reports(token)
    
    print("\nTests completed.")

if __name__ == "__main__":
    main()
