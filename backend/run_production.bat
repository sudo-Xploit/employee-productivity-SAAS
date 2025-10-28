@echo off
echo Starting Employee Productivity API in production mode...

REM Check if port 8000 is already in use
netstat -ano | findstr :8000 | findstr LISTENING > nul
if %ERRORLEVEL% EQU 0 (
    echo Port 8000 is already in use. Killing existing processes...
    call kill_port.bat
    timeout /t 2 /nobreak > nul
)

REM Set environment variables for production
set LOG_LEVEL=INFO
set JSON_LOGS=true
set ENABLE_METRICS=true
set HEALTH_CHECK_INCLUDE_DB=true
set DB_POOL_SIZE=10
set DB_MAX_OVERFLOW=20
set DB_POOL_TIMEOUT=30
set DB_POOL_RECYCLE=1800
set DB_ECHO=false

REM Create necessary directories
if not exist "reports" mkdir reports
if not exist "models" mkdir models

echo Starting server...
echo API will be available at http://localhost:8000
echo Documentation at http://localhost:8000/docs
echo Health check at http://localhost:8000/api/v1/health

REM Start the application with uvicorn for testing or gunicorn for production
if "%1"=="--test" (
    echo Running in test mode with uvicorn...
    uvicorn app.main_production:app --host 0.0.0.0 --port 8000 --log-level info
) else (
    echo Running in production mode with gunicorn...
    gunicorn app.main_production:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --workers 4 --worker-tmp-dir /dev/shm --log-level info
)
