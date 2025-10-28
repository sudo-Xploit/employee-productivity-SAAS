# Employee Productivity API Documentation

This document provides comprehensive documentation for the Employee Productivity API endpoints, authentication, and data models to assist with frontend integration.

## Base URL

The API base URL is: `http://localhost:8000`

API version prefix: `/api/v1`

## Authentication

### Register a New User

```
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword",
  "full_name": "John Doe",
  "role": "ANALYST"  // Options: "ADMIN", "DEPARTMENT_HEAD", "ANALYST", "READ_ONLY"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "ANALYST",
  "is_active": true
}
```

### Login

```
POST /api/v1/auth/login
```

**Request Body:**
```
username=user@example.com&password=strongpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Refresh Token

```
POST /api/v1/auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```
GET /api/v1/auth/me
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "ANALYST",
  "is_active": true
}
```

## Departments

### List All Departments

```
GET /api/v1/departments
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Engineering",
    "budget": 500000,
    "created_at": "2025-10-28T12:00:00"
  },
  {
    "id": 2,
    "name": "Marketing",
    "budget": 300000,
    "created_at": "2025-10-28T12:00:00"
  }
]
```

### Get Department by ID

```
GET /api/v1/departments/{department_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "name": "Engineering",
  "budget": 500000,
  "created_at": "2025-10-28T12:00:00"
}
```

### Create Department

```
POST /api/v1/departments
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Research",
  "budget": 400000
}
```

**Response:**
```json
{
  "id": 3,
  "name": "Research",
  "budget": 400000,
  "created_at": "2025-10-28T12:00:00"
}
```

### Update Department

```
PUT /api/v1/departments/{department_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Research & Development",
  "budget": 450000
}
```

**Response:**
```json
{
  "id": 3,
  "name": "Research & Development",
  "budget": 450000,
  "created_at": "2025-10-28T12:00:00"
}
```

### Delete Department

```
DELETE /api/v1/departments/{department_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 3,
  "name": "Research & Development",
  "budget": 450000,
  "created_at": "2025-10-28T12:00:00"
}
```

## Employees

### List All Employees

```
GET /api/v1/employees
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "department_id": 1,
    "salary": 85000,
    "hire_date": "2023-01-15",
    "created_at": "2025-10-28T12:00:00"
  }
]
```

### Get Employee by ID

```
GET /api/v1/employees/{employee_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "john@example.com",
  "department_id": 1,
  "salary": 85000,
  "hire_date": "2023-01-15",
  "created_at": "2025-10-28T12:00:00",
  "department": {
    "id": 1,
    "name": "Engineering"
  }
}
```

### Create Employee

```
POST /api/v1/employees
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "department_id": 2,
  "salary": 75000,
  "hire_date": "2023-05-20"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "department_id": 2,
  "salary": 75000,
  "hire_date": "2023-05-20",
  "created_at": "2025-10-28T12:00:00"
}
```

### Update Employee

```
PUT /api/v1/employees/{employee_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "department_id": 2,
  "salary": 80000,
  "hire_date": "2023-05-20"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "department_id": 2,
  "salary": 80000,
  "hire_date": "2023-05-20",
  "created_at": "2025-10-28T12:00:00"
}
```

### Delete Employee

```
DELETE /api/v1/employees/{employee_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "department_id": 2,
  "salary": 80000,
  "hire_date": "2023-05-20",
  "created_at": "2025-10-28T12:00:00"
}
```

## Projects

### List All Projects

```
GET /api/v1/projects
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Website Redesign",
    "budget": 50000,
    "start_date": "2023-02-01",
    "end_date": "2023-05-01",
    "status": "COMPLETED",
    "department_id": 2,
    "created_at": "2025-10-28T12:00:00"
  }
]
```

### Get Project by ID

```
GET /api/v1/projects/{project_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "name": "Website Redesign",
  "budget": 50000,
  "start_date": "2023-02-01",
  "end_date": "2023-05-01",
  "status": "COMPLETED",
  "department_id": 2,
  "created_at": "2025-10-28T12:00:00",
  "department": {
    "id": 2,
    "name": "Marketing"
  }
}
```

### Create Project

```
POST /api/v1/projects
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "Mobile App Development",
  "budget": 120000,
  "start_date": "2023-06-01",
  "end_date": "2023-12-01",
  "status": "IN_PROGRESS",
  "department_id": 1
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Mobile App Development",
  "budget": 120000,
  "start_date": "2023-06-01",
  "end_date": "2023-12-01",
  "status": "IN_PROGRESS",
  "department_id": 1,
  "created_at": "2025-10-28T12:00:00"
}
```

## Timesheets

### List All Timesheets

```
GET /api/v1/timesheets
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "employee_id": 1,
    "project_id": 1,
    "date": "2023-03-15",
    "hours": 8,
    "description": "Frontend development",
    "created_at": "2025-10-28T12:00:00"
  }
]
```

### Create Timesheet Entry

```
POST /api/v1/timesheets
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "employee_id": 1,
  "project_id": 2,
  "date": "2023-06-15",
  "hours": 6,
  "description": "API development"
}
```

**Response:**
```json
{
  "id": 2,
  "employee_id": 1,
  "project_id": 2,
  "date": "2023-06-15",
  "hours": 6,
  "description": "API development",
  "created_at": "2025-10-28T12:00:00"
}
```

## Analytics

### Company Analytics

```
GET /api/v1/analytics/company
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "total_employees": 10,
  "total_departments": 3,
  "total_projects": 5,
  "total_budget": 1200000,
  "total_salary": 850000,
  "total_hours_logged": 1500,
  "average_productivity_index": 2.3,
  "roi": 0.41
}
```

### Department Analytics

```
GET /api/v1/analytics/departments/{department_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "department_id": 1,
  "department_name": "Engineering",
  "employee_count": 5,
  "project_count": 3,
  "budget": 500000,
  "total_salary": 425000,
  "total_hours_logged": 800,
  "productivity_index": 2.5,
  "roi": 0.18
}
```

### Top Performers

```
GET /api/v1/analytics/top-performers
```

**Query Parameters:**
- `limit` (optional): Number of top performers to return (default: 5, max: 20)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "employee_id": 1,
    "name": "John Smith",
    "department": "Engineering",
    "productivity_index": 3.2,
    "hours_logged": 160,
    "revenue_generated": 85000
  }
]
```

## Reports

### Generate Report

```
GET /api/v1/reports/generate
```

**Query Parameters:**
- `report_type`: Type of report to generate (`pdf` or `excel`)

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
File download (PDF or Excel)

## File Uploads

### Upload CSV

```
POST /api/v1/upload/{entity}
```

Where `{entity}` is one of: `employees`, `projects`, or `timesheets`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Form Data:**
```
file: [CSV file]
```

**Response:**
```json
{
  "message": "Import successful",
  "imported": 5,
  "failed": 0
}
```

## ML Predictions

### Predict Department Performance

```
GET /api/v1/predict/department/{department_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "success": true,
  "department_id": 1,
  "department_name": "Engineering",
  "predictions": {
    "roi": {
      "current": 0.18,
      "predicted": 0.22,
      "trend": 0.04,
      "trend_percentage": 22.2,
      "confidence": 0.85
    },
    "cost": {
      "current": 425000,
      "predicted": 440000,
      "trend": 15000,
      "trend_percentage": 3.5,
      "confidence": 0.92
    }
  },
  "recommendations": [
    "Consider allocating more resources to the mobile app project to improve ROI",
    "Team productivity is trending upward, maintain current management approach"
  ]
}
```

### Train Department Model

```
POST /api/v1/predict/department/{department_id}/train
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "message": "Department prediction models trained successfully",
  "department_id": 1,
  "department_name": "Engineering",
  "roi_model_metrics": {
    "r2_score": 0.87,
    "mean_absolute_error": 0.02
  },
  "cost_model_metrics": {
    "r2_score": 0.91,
    "mean_absolute_error": 5000
  }
}
```

## Health Check

```
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-28T16:30:00.000Z",
  "version": "1.0.0",
  "system": {
    "os": "Windows",
    "python_version": "3.11.0"
  },
  "resources": {
    "cpu_usage": 15.2,
    "memory": {
      "total": 16000000000,
      "available": 8000000000,
      "percent_used": 50.0
    },
    "disk": {
      "total": 500000000000,
      "free": 250000000000,
      "percent_used": 50.0
    }
  },
  "directories": {
    "reports": true,
    "models": true
  },
  "database": {
    "status": "connected"
  }
}
```

## Error Handling

All API endpoints follow a consistent error response format:

```json
{
  "detail": "Error message or object with details"
}
```

Common HTTP status codes:
- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server-side error

## CORS Configuration

The API supports CORS for frontend integration. The default configuration allows requests from:
- http://localhost:3000
- http://127.0.0.1:3000
- http://localhost:5173
- http://127.0.0.1:5173

To modify the CORS configuration, edit the `cors.json` file in the backend directory.
