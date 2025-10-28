import pytest
from fastapi.testclient import TestClient


@pytest.mark.crud
class TestDepartmentCRUD:
    """Test CRUD operations for departments"""
    
    @pytest.mark.parametrize("role_headers", ["admin_token_headers", "department_head_token_headers"])
    def test_create_department(self, client, request, role_headers):
        """Test creating a department"""
        headers = request.getfixturevalue(role_headers)
        department_data = {
            "name": "Test Department",
            "budget": 100000.0
        }
        
        response = client.post(
            "/api/v1/departments/", 
            json=department_data,
            headers=headers
        )
        assert response.status_code == 200
        
        created_dept = response.json()
        assert created_dept["name"] == department_data["name"]
        assert created_dept["budget"] == department_data["budget"]
        assert "id" in created_dept
    
    def test_get_departments(self, client, user_token_headers):
        """Test getting all departments"""
        response = client.get("/api/v1/departments/", headers=user_token_headers)
        assert response.status_code == 200
        
        departments = response.json()
        assert isinstance(departments, list)
        assert len(departments) >= 2  # We created at least 2 in the fixtures
        
        # Check structure of first department
        dept = departments[0]
        assert "id" in dept
        assert "name" in dept
        assert "budget" in dept
    
    def test_get_department(self, client, user_token_headers):
        """Test getting a specific department"""
        response = client.get("/api/v1/departments/1", headers=user_token_headers)
        assert response.status_code == 200
        
        dept = response.json()
        assert dept["id"] == 1
        assert dept["name"] == "Engineering"
        assert dept["budget"] == 500000.0
    
    def test_update_department(self, client, admin_token_headers):
        """Test updating a department"""
        update_data = {
            "name": "Updated Engineering",
            "budget": 550000.0
        }
        
        response = client.put(
            "/api/v1/departments/1", 
            json=update_data,
            headers=admin_token_headers
        )
        assert response.status_code == 200
        
        updated_dept = response.json()
        assert updated_dept["id"] == 1
        assert updated_dept["name"] == update_data["name"]
        assert updated_dept["budget"] == update_data["budget"]
    
    def test_delete_department(self, client, admin_token_headers):
        """Test deleting a department"""
        # First create a department to delete
        department_data = {
            "name": "Department to Delete",
            "budget": 50000.0
        }
        
        create_response = client.post(
            "/api/v1/departments/", 
            json=department_data,
            headers=admin_token_headers
        )
        created_dept = create_response.json()
        dept_id = created_dept["id"]
        
        # Now delete it
        delete_response = client.delete(
            f"/api/v1/departments/{dept_id}", 
            headers=admin_token_headers
        )
        assert delete_response.status_code == 200
        
        # Verify it's deleted
        get_response = client.get(
            f"/api/v1/departments/{dept_id}", 
            headers=admin_token_headers
        )
        assert get_response.status_code == 404


@pytest.mark.crud
class TestEmployeeCRUD:
    """Test CRUD operations for employees"""
    
    def test_create_employee(self, client, department_head_token_headers):
        """Test creating an employee"""
        employee_data = {
            "name": "Test Employee",
            "department_id": 1,
            "salary": 90000.0,
            "revenue_generated": 180000.0
        }
        
        response = client.post(
            "/api/v1/employees/", 
            json=employee_data,
            headers=department_head_token_headers
        )
        assert response.status_code == 200
        
        created_emp = response.json()
        assert created_emp["name"] == employee_data["name"]
        assert created_emp["department_id"] == employee_data["department_id"]
        assert created_emp["salary"] == employee_data["salary"]
        assert created_emp["revenue_generated"] == employee_data["revenue_generated"]
        assert "id" in created_emp
    
    def test_get_employees(self, client, user_token_headers):
        """Test getting all employees"""
        response = client.get("/api/v1/employees/", headers=user_token_headers)
        assert response.status_code == 200
        
        employees = response.json()
        assert isinstance(employees, list)
        assert len(employees) >= 3  # We created at least 3 in the fixtures
        
        # Check structure of first employee
        emp = employees[0]
        assert "id" in emp
        assert "name" in emp
        assert "department_id" in emp
        assert "salary" in emp
    
    def test_get_employee(self, client, user_token_headers):
        """Test getting a specific employee"""
        response = client.get("/api/v1/employees/1", headers=user_token_headers)
        assert response.status_code == 200
        
        emp = response.json()
        assert emp["id"] == 1
        assert emp["name"] == "John Smith"
        assert emp["department_id"] == 1
        assert emp["salary"] == 120000.0
    
    def test_update_employee(self, client, department_head_token_headers):
        """Test updating an employee"""
        update_data = {
            "name": "Updated John Smith",
            "salary": 125000.0
        }
        
        response = client.put(
            "/api/v1/employees/1", 
            json=update_data,
            headers=department_head_token_headers
        )
        assert response.status_code == 200
        
        updated_emp = response.json()
        assert updated_emp["id"] == 1
        assert updated_emp["name"] == update_data["name"]
        assert updated_emp["salary"] == update_data["salary"]
        # Other fields should remain unchanged
        assert updated_emp["department_id"] == 1
    
    def test_delete_employee(self, client, admin_token_headers):
        """Test deleting an employee"""
        # First create an employee to delete
        employee_data = {
            "name": "Employee to Delete",
            "department_id": 1,
            "salary": 80000.0,
            "revenue_generated": 160000.0
        }
        
        create_response = client.post(
            "/api/v1/employees/", 
            json=employee_data,
            headers=admin_token_headers
        )
        created_emp = create_response.json()
        emp_id = created_emp["id"]
        
        # Now delete it
        delete_response = client.delete(
            f"/api/v1/employees/{emp_id}", 
            headers=admin_token_headers
        )
        assert delete_response.status_code == 200
        
        # Verify it's deleted
        get_response = client.get(
            f"/api/v1/employees/{emp_id}", 
            headers=admin_token_headers
        )
        assert get_response.status_code == 404


@pytest.mark.crud
class TestProjectCRUD:
    """Test CRUD operations for projects"""
    
    def test_create_project(self, client, department_head_token_headers):
        """Test creating a project"""
        project_data = {
            "name": "Test Project",
            "department_id": 1,
            "cost": 30000.0,
            "revenue": 90000.0
        }
        
        response = client.post(
            "/api/v1/projects/", 
            json=project_data,
            headers=department_head_token_headers
        )
        assert response.status_code == 200
        
        created_proj = response.json()
        assert created_proj["name"] == project_data["name"]
        assert created_proj["department_id"] == project_data["department_id"]
        assert created_proj["cost"] == project_data["cost"]
        assert created_proj["revenue"] == project_data["revenue"]
        assert "id" in created_proj
    
    def test_get_projects(self, client, user_token_headers):
        """Test getting all projects"""
        response = client.get("/api/v1/projects/", headers=user_token_headers)
        assert response.status_code == 200
        
        projects = response.json()
        assert isinstance(projects, list)
        assert len(projects) >= 3  # We created at least 3 in the fixtures
        
        # Check structure of first project
        proj = projects[0]
        assert "id" in proj
        assert "name" in proj
        assert "department_id" in proj
        assert "cost" in proj
        assert "revenue" in proj
    
    def test_get_project(self, client, user_token_headers):
        """Test getting a specific project"""
        response = client.get("/api/v1/projects/1", headers=user_token_headers)
        assert response.status_code == 200
        
        proj = response.json()
        assert proj["id"] == 1
        assert proj["name"] == "Product Redesign"
        assert proj["department_id"] == 1
        assert proj["cost"] == 50000.0
        assert proj["revenue"] == 150000.0
    
    def test_update_project(self, client, department_head_token_headers):
        """Test updating a project"""
        update_data = {
            "name": "Updated Product Redesign",
            "cost": 55000.0,
            "revenue": 160000.0
        }
        
        response = client.put(
            "/api/v1/projects/1", 
            json=update_data,
            headers=department_head_token_headers
        )
        assert response.status_code == 200
        
        updated_proj = response.json()
        assert updated_proj["id"] == 1
        assert updated_proj["name"] == update_data["name"]
        assert updated_proj["cost"] == update_data["cost"]
        assert updated_proj["revenue"] == update_data["revenue"]
        # Other fields should remain unchanged
        assert updated_proj["department_id"] == 1
    
    def test_delete_project(self, client, admin_token_headers):
        """Test deleting a project"""
        # First create a project to delete
        project_data = {
            "name": "Project to Delete",
            "department_id": 1,
            "cost": 20000.0,
            "revenue": 60000.0
        }
        
        create_response = client.post(
            "/api/v1/projects/", 
            json=project_data,
            headers=admin_token_headers
        )
        created_proj = create_response.json()
        proj_id = created_proj["id"]
        
        # Now delete it
        delete_response = client.delete(
            f"/api/v1/projects/{proj_id}", 
            headers=admin_token_headers
        )
        assert delete_response.status_code == 200
        
        # Verify it's deleted
        get_response = client.get(
            f"/api/v1/projects/{proj_id}", 
            headers=admin_token_headers
        )
        assert get_response.status_code == 404
