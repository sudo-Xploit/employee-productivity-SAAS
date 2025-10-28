# Employee Productivity & Cost Analysis Platform

![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-009688?style=flat-square&logo=fastapi) ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker) ![ML](https://img.shields.io/badge/ML-Predictions-FF6F00?style=flat-square&logo=tensorflow)

A powerful FastAPI backend for analyzing employee productivity, project profitability, and department efficiency. This enterprise-grade SaaS solution helps businesses make data-driven decisions through advanced analytics and machine learning predictions.

## 🚀 Key Features

### Core Functionality
- **Employee & Department Management** - Track performance metrics, salaries, and organizational structure
- **Project & Timesheet Tracking** - Monitor costs, revenue, and resource allocation
- **Advanced Analytics** - Comprehensive metrics with ROI calculations and productivity indices
- **ML Predictions** - Forecast future performance based on historical patterns
- **Multi-format Reporting** - Generate PDF, Excel, CSV, and TXT reports with visualizations

### Technical Excellence
- **Secure Authentication** - JWT with refresh tokens and role-based access control
- **High Performance** - Async endpoints, connection pooling, and optimized queries
- **Enterprise Monitoring** - Prometheus metrics, health checks, and structured logging
- **Production Ready** - Docker, Kubernetes support, and comprehensive security headers
- **Developer Experience** - Enhanced OpenAPI docs, error handling, and clean architecture

## 🏗️ Architecture

The project follows a clean, modular architecture with clear separation of concerns:

```
backend/
├── app/
│   ├── api/v1/         # API endpoints with routers, schemas, dependencies
│   ├── core/           # Configuration, security, logging, metrics
│   ├── db/             # Database session, models, migrations
│   ├── models/         # SQLAlchemy ORM models
│   ├── services/       # Business logic layer
│   └── main_production.py  # Application entry point
├── tests/             # Comprehensive test suite
├── helm/              # Kubernetes deployment
├── prometheus/        # Monitoring configuration
└── docker-compose.yml # Container orchestration
```

The system implements a layered architecture:
- **API Layer**: Request handling, validation, and response formatting
- **Service Layer**: Business logic and domain rules
- **Data Access Layer**: Database operations and ORM models
- **Infrastructure Layer**: Configuration, logging, metrics, and security

## 🔧 Quick Start

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# 1. Install dependencies and set up database
.\setup.bat

# 2. (Optional) Seed with sample data
.\seed_db.bat

# 3. Start the application
.\run_app.bat         # Development mode
.\run_dev_enhanced.bat  # Development with metrics
.\run_production.bat    # Production mode
```

The setup script automatically installs dependencies, creates database tables, sets up required directories, and runs migrations.

## 🔗 Integration

### Frontend Development

```bash
# API Documentation
http://localhost:8000/docs  # Swagger UI
http://localhost:8000/redoc # ReDoc
```

Key resources for frontend developers:
- **Integration Guide**: See `FRONTEND_INTEGRATION.md`
- **CORS Support**: Pre-configured for common dev servers
- **Authentication**: JWT with refresh token mechanism

### Containerization

```bash
# Docker Compose
docker-compose up api-dev      # Development
docker-compose up api-prod     # Production
docker-compose up prometheus grafana  # Monitoring

# Kubernetes
helm install employee-productivity-api ./helm
```

## 💯 Core Features

### Authentication & Access Control

```bash
POST /api/v1/auth/register  # Create new user
POST /api/v1/auth/login     # Get access & refresh tokens
POST /api/v1/auth/refresh   # Refresh expired token
```

Four role levels with granular permissions:
- **Admin**: Full system access
- **Department Head**: Department-specific management
- **Analyst**: Analytics and reporting access
- **Read-Only**: Basic data viewing

### Analytics & Insights

```bash
GET /api/v1/analytics/company                # Company-wide metrics
GET /api/v1/analytics/departments/{id}       # Department performance
GET /api/v1/analytics/employees/{id}         # Employee metrics
GET /api/v1/analytics/top-performers         # Ranking by performance
```

Key metrics calculated automatically:
- **ROI**: (Revenue - Cost) / Cost
- **Productivity Index**: Revenue / Hours
- **Budget Utilization**: Spent / Allocated

### Data Management

```bash
# Bulk imports with validation
POST /api/v1/upload/employees    # Employee data
POST /api/v1/upload/projects     # Project data
POST /api/v1/upload/timesheets   # Time tracking data

# Multi-format reporting
GET /api/v1/reports/generate?report_type=pdf   # PDF reports
GET /api/v1/reports/generate?report_type=excel # Excel reports
```

### ML Predictions

```bash
GET /api/v1/predict/department/{id}  # Department forecasts
GET /api/v1/predict/employee/{id}    # Employee performance prediction
GET /api/v1/predict/project/{id}     # Project outcome prediction
POST /api/v1/predict/train           # Retrain ML models
```

## 🛠 DevOps & Monitoring

### Health & Metrics

```bash
GET /api/v1/health  # System health with resource metrics
GET /metrics        # Prometheus metrics endpoint
```

Comprehensive monitoring includes:
- **Health Checks**: Database, disk, memory, CPU, directories
- **Metrics**: Request counts, latencies, connection pools
- **Visualization**: Grafana dashboards for key metrics
- **Logging**: Structured JSON logs with correlation IDs


## 📜 License

MIT License

---

<p align="center">
  <i>Built with FastAPI, SQLAlchemy, and ML-powered analytics</i><br>
  <i>© 2025 Exo Delta</i>
</p>
