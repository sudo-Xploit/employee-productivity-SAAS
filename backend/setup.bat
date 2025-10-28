@echo off
echo ======================================================
echo Employee Productivity API - Setup Script
echo ======================================================
echo.

echo Step 1: Installing dependencies...
call install_deps.bat
echo.

echo Step 2: Setting up database...
python setup_db.py
echo.

echo Step 3: Creating necessary directories...
if not exist "reports" mkdir reports
if not exist "models" mkdir models
echo Directories created.
echo.

echo Step 4: Creating .env file if it doesn't exist...
if not exist ".env" (
    echo Creating default .env file...
    echo DATABASE_URL=sqlite:///./sql_app.db > .env
    echo SECRET_KEY=temporarysecretkey >> .env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=1440 >> .env
    echo REFRESH_TOKEN_EXPIRE_DAYS=30 >> .env
    echo BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000","http://localhost:5173","http://127.0.0.1:5173"] >> .env
    echo LOG_LEVEL=INFO >> .env
    echo JSON_LOGS=true >> .env
    echo ENABLE_METRICS=true >> .env
    echo HEALTH_CHECK_INCLUDE_DB=true >> .env
    echo DB_POOL_SIZE=5 >> .env
    echo DB_MAX_OVERFLOW=10 >> .env
    echo DB_POOL_TIMEOUT=30 >> .env
    echo DB_POOL_RECYCLE=1800 >> .env
    echo DB_ECHO=false >> .env
    echo FIRST_SUPERUSER=admin@example.com >> .env
    echo FIRST_SUPERUSER_PASSWORD=admin >> .env
    echo .env file created with default settings.
) else (
    echo .env file already exists, skipping creation.
)
echo.

echo Step 5: Running database migrations...
call run_upgrade.bat
echo.

echo ======================================================
echo Setup complete!
echo.
echo You can now run the API using:
echo   .\run_production.bat --test    (for development)
echo   .\run_production.bat           (for production)
echo.
echo API will be available at http://localhost:8000
echo Documentation at http://localhost:8000/docs
echo Health check at http://localhost:8000/api/v1/health
echo ======================================================
