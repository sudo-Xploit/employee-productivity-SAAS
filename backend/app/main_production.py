import os
import uuid
import time
import shutil
import platform
import psutil
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from typing import Callable, Dict, Any, List, Optional

from app.core.config import settings
from app.core.logging import setup_logging, get_logger, get_request_logger
from app.core.metrics import setup_metrics
from app.db.base_class import Base
from app.db.session import engine, get_db, SessionLocal
from app.api.v1.routers import auth, departments, employees, projects, analytics, reports, uploads, timesheets, predictions

# Set up logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist
    logger.info("Creating database tables if they don't exist")
    Base.metadata.create_all(bind=engine)
    
    # Create necessary directories
    logger.info("Setting up application directories")
    reports_dir = os.path.join(os.getcwd(), "reports")
    models_dir = os.path.join(os.getcwd(), "models")
    
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        logger.info(f"Created reports directory: {reports_dir}")
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        logger.info(f"Created models directory: {models_dir}")
    
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")

app = FastAPI(
    title="Employee Productivity API",
    description="Employee Productivity and Cost Analysis API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up Prometheus metrics if enabled
if settings.ENABLE_METRICS:
    setup_metrics(app)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next: Callable) -> Response:
    response = await call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    
    return response

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    """Middleware to log all requests."""
    # Generate a unique request ID
    request_id = str(uuid.uuid4())
    
    # Create a logger with request context
    request_logger = get_request_logger(request_id)
    
    # Log request details
    request_logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_host": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        },
    )
    
    # Process the request
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response details
        request_logger.info(
            f"Request completed: {request.method} {request.url.path} {response.status_code}",
            extra={
                "status_code": response.status_code,
                "processing_time_ms": round(process_time * 1000, 2),
            },
        )
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    except Exception as e:
        # Log exception details
        process_time = time.time() - start_time
        request_logger.error(
            f"Request failed: {request.method} {request.url.path}",
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "processing_time_ms": round(process_time * 1000, 2),
            },
            exc_info=True,
        )
        raise

# Mount reports directory as static files
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Custom OpenAPI schema with tag ordering and descriptions
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add OpenAPI version
    openapi_schema.update({"openapi": "3.0.0"})

    # Add tag metadata for better documentation organization
    openapi_schema["tags"] = [
        {"name": "auth", "description": "Authentication and authorization operations"},
        {"name": "departments", "description": "Department management operations"},
        {"name": "employees", "description": "Employee management operations"},
        {"name": "projects", "description": "Project management operations"},
        {"name": "timesheets", "description": "Timesheet tracking operations"},
        {"name": "analytics", "description": "Analytics and data visualization operations"},
        {"name": "reports", "description": "Report generation operations"},
        {"name": "uploads", "description": "File upload operations"},
        {"name": "predictions", "description": "ML predictions and model training operations"},
        {"name": "health", "description": "Health check and monitoring endpoints"},
    ]

    # Add security scheme for JWT
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers with organized tags
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(departments.router, prefix=f"{settings.API_V1_STR}/departments", tags=["departments"])
app.include_router(employees.router, prefix=f"{settings.API_V1_STR}/employees", tags=["employees"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(timesheets.router, prefix=f"{settings.API_V1_STR}/timesheets", tags=["timesheets"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])
app.include_router(uploads.router, prefix=f"{settings.API_V1_STR}/upload", tags=["uploads"])
app.include_router(predictions.router, prefix=f"{settings.API_V1_STR}/predict", tags=["predictions"])

# Custom documentation endpoints
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Employee Productivity API",
        "version": app.version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_check": f"{settings.API_V1_STR}/health",
    }

# Comprehensive health check endpoint
@app.get(f"{settings.API_V1_STR}/health", tags=["health"])
def health_check():
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": app.version,
        "system": {
            "os": platform.system(),
            "python_version": platform.python_version(),
        },
        "resources": {
            "cpu_usage": psutil.cpu_percent(),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent_used": psutil.virtual_memory().percent,
            },
            "disk": {
                "total": shutil.disk_usage("/").total,
                "free": shutil.disk_usage("/").free,
                "percent_used": (shutil.disk_usage("/").used / shutil.disk_usage("/").total) * 100,
            },
        },
        "directories": {
            "reports": os.path.exists("reports"),
            "models": os.path.exists("models"),
        },
    }
    
    # Check database connection if enabled
    if settings.HEALTH_CHECK_INCLUDE_DB:
        try:
            # Create a new session for the health check
            db = SessionLocal()
            # Execute a simple query to check DB connection
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            health_data["database"] = {"status": "connected"}
            # Close the session
            db.close()
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            health_data["status"] = "unhealthy"
            health_data["database"] = {
                "status": "disconnected",
                "error": str(e),
            }
            # Don't raise an exception, just report the database issue
            # This allows the health check to still return other system information
    
    return health_data
