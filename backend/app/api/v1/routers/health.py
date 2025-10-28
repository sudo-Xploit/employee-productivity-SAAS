import os
import time
import psutil
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.core.config import settings
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", summary="Health check endpoint")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Health check endpoint that returns the status of various system components.
    
    Returns:
        Dict[str, Any]: Health check results
    """
    start_time = time.time()
    health_data = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "checks": []
    }
    
    # Check database connection
    if settings.HEALTH_CHECK_INCLUDE_DB:
        try:
            # Execute a simple query to check database connection
            result = db.execute(text("SELECT 1")).scalar()
            db_status = "healthy" if result == 1 else "unhealthy"
            health_data["checks"].append({
                "name": "database",
                "status": db_status,
                "message": "Database connection successful" if db_status == "healthy" else "Database connection failed"
            })
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            health_data["checks"].append({
                "name": "database",
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}"
            })
            health_data["status"] = "unhealthy"
    
    # Check disk space
    try:
        disk_usage = psutil.disk_usage("/")
        disk_percent = disk_usage.percent
        disk_status = "healthy" if disk_percent < 90 else "warning" if disk_percent < 95 else "unhealthy"
        health_data["checks"].append({
            "name": "disk",
            "status": disk_status,
            "message": f"Disk usage: {disk_percent:.1f}%",
            "details": {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percent": disk_usage.percent
            }
        })
        if disk_status == "unhealthy":
            health_data["status"] = "unhealthy"
        elif disk_status == "warning" and health_data["status"] != "unhealthy":
            health_data["status"] = "warning"
    except Exception as e:
        logger.error(f"Disk health check failed: {str(e)}")
        health_data["checks"].append({
            "name": "disk",
            "status": "unknown",
            "message": f"Disk check failed: {str(e)}"
        })
    
    # Check memory usage
    try:
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_status = "healthy" if memory_percent < 90 else "warning" if memory_percent < 95 else "unhealthy"
        health_data["checks"].append({
            "name": "memory",
            "status": memory_status,
            "message": f"Memory usage: {memory_percent:.1f}%",
            "details": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent
            }
        })
        if memory_status == "unhealthy":
            health_data["status"] = "unhealthy"
        elif memory_status == "warning" and health_data["status"] != "unhealthy":
            health_data["status"] = "warning"
    except Exception as e:
        logger.error(f"Memory health check failed: {str(e)}")
        health_data["checks"].append({
            "name": "memory",
            "status": "unknown",
            "message": f"Memory check failed: {str(e)}"
        })
    
    # Check CPU usage
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_status = "healthy" if cpu_percent < 90 else "warning" if cpu_percent < 95 else "unhealthy"
        health_data["checks"].append({
            "name": "cpu",
            "status": cpu_status,
            "message": f"CPU usage: {cpu_percent:.1f}%",
            "details": {
                "percent": cpu_percent,
                "cores": psutil.cpu_count()
            }
        })
        if cpu_status == "unhealthy":
            health_data["status"] = "unhealthy"
        elif cpu_status == "warning" and health_data["status"] != "unhealthy":
            health_data["status"] = "warning"
    except Exception as e:
        logger.error(f"CPU health check failed: {str(e)}")
        health_data["checks"].append({
            "name": "cpu",
            "status": "unknown",
            "message": f"CPU check failed: {str(e)}"
        })
    
    # Check if required directories exist
    required_dirs = ["reports", "models"]
    missing_dirs = []
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        health_data["checks"].append({
            "name": "directories",
            "status": "warning",
            "message": f"Missing directories: {', '.join(missing_dirs)}",
            "details": {
                "missing": missing_dirs,
                "required": required_dirs
            }
        })
        if health_data["status"] != "unhealthy":
            health_data["status"] = "warning"
    else:
        health_data["checks"].append({
            "name": "directories",
            "status": "healthy",
            "message": "All required directories exist"
        })
    
    # Add response time
    health_data["response_time_ms"] = int((time.time() - start_time) * 1000)
    
    return health_data


@router.get("/ping", summary="Simple ping endpoint")
async def ping() -> Dict[str, str]:
    """
    Simple ping endpoint for basic connectivity checks.
    
    Returns:
        Dict[str, str]: Simple status message
    """
    return {"status": "ok"}
