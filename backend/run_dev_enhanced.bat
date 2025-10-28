@echo off
echo Starting Employee Productivity API in development mode with enhanced features...

REM Set environment variables for development
set LOG_LEVEL=DEBUG
set JSON_LOGS=false
set ENABLE_METRICS=true
set HEALTH_CHECK_INCLUDE_DB=true
set DB_POOL_SIZE=5
set DB_MAX_OVERFLOW=10
set DB_POOL_TIMEOUT=30
set DB_POOL_RECYCLE=1800
set DB_ECHO=true

REM Start the application with uvicorn in reload mode
uvicorn app.main_production:app --reload --host 0.0.0.0 --port 8000 --log-level debug
