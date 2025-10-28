FROM python:3.11-slim as builder

WORKDIR /app/

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app/

# Create a non-root user
RUN addgroup --system app && \
    adduser --system --group app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Install gunicorn
RUN pip install gunicorn

# Copy project
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/reports /app/models
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    LOG_LEVEL=INFO \
    JSON_LOGS=true \
    ENABLE_METRICS=true \
    HEALTH_CHECK_INCLUDE_DB=true \
    DB_POOL_SIZE=10 \
    DB_MAX_OVERFLOW=20 \
    DB_POOL_TIMEOUT=30 \
    DB_POOL_RECYCLE=1800 \
    DB_ECHO=false

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/ping || exit 1

# Expose port
EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "app.main_production:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "4", "--worker-tmp-dir", "/dev/shm", "--log-level", "info"]