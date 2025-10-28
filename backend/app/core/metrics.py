from typing import Callable, Dict, Optional
import time
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

# Define metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress",
    ["method", "endpoint"]
)

DB_CONNECTION_POOL = Gauge(
    "db_connection_pool",
    "Database connection pool statistics",
    ["state"]  # 'total', 'used', 'idle'
)

API_INFO = Info(
    "api_info",
    "API information"
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Middleware to collect Prometheus metrics for HTTP requests.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Skip metrics endpoint to avoid recursion
        if request.url.path == "/metrics":
            return await call_next(request)
        
        method = request.method
        endpoint = request.url.path
        
        # Track request in progress
        REQUESTS_IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()
        
        # Track request latency
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status_code = response.status_code
            
            # Record request count and latency
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
            
            return response
        except Exception as e:
            # Record request count for exceptions
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=500).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
            raise e
        finally:
            # Track request completion
            REQUESTS_IN_PROGRESS.labels(method=method, endpoint=endpoint).dec()


def set_api_info(app_name: str, version: str) -> None:
    """
    Set API information metric.
    """
    API_INFO.info({"app_name": app_name, "version": version})


def update_db_pool_metrics(total: int, used: int, idle: int) -> None:
    """
    Update database connection pool metrics.
    """
    DB_CONNECTION_POOL.labels(state="total").set(total)
    DB_CONNECTION_POOL.labels(state="used").set(used)
    DB_CONNECTION_POOL.labels(state="idle").set(idle)


def setup_metrics(app: FastAPI) -> None:
    """
    Set up Prometheus metrics for the FastAPI application.
    """
    # Add Prometheus middleware
    app.add_middleware(PrometheusMiddleware)
    
    # Add metrics endpoint
    @app.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
    
    # Set API info
    set_api_info(app.title, "1.0.0")
