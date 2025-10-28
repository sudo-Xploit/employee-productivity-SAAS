from typing import Callable, Dict

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from app.core.config import settings


# Create rate limiter
limiter = Limiter(key_func=get_remote_address)


def setup_middlewares(app: FastAPI) -> None:
    """Set up all middlewares for the application."""
    # Set up CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Set up rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)


async def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Handler for rate limit exceeded exceptions."""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded",
            "retry_after": exc.retry_after
        },
        headers={"Retry-After": str(exc.retry_after)}
    )


# Decorator for applying rate limits to specific endpoints
def rate_limit(
    limit_per_minute: int = settings.RATE_LIMIT_PER_MINUTE,
    limit_per_hour: int = settings.RATE_LIMIT_PER_HOUR
) -> Callable:
    """
    Apply rate limiting to a specific endpoint.
    
    Example usage:
    
    @router.get("/endpoint")
    @rate_limit(limit_per_minute=10, limit_per_hour=100)
    def endpoint():
        return {"message": "Rate limited endpoint"}
    """
    def decorator(func: Callable) -> Callable:
        # Apply minute limit
        func = limiter.limit(f"{limit_per_minute}/minute")(func)
        # Apply hour limit
        func = limiter.limit(f"{limit_per_hour}/hour")(func)
        return func
    
    return decorator
