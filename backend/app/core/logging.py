import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from app.core.config import settings


class JSONLogFormatter(logging.Formatter):
    """
    Custom JSON log formatter for structured logging.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_record["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }
        
        # Add extra fields if present
        if hasattr(record, "extra"):
            log_record.update(record.extra)
        
        return json.dumps(log_record)


def setup_logging() -> None:
    """
    Set up logging configuration based on settings.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Clear existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    
    # Configure root logger
    root_logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Set formatter based on settings
    if settings.JSON_LOGS:
        formatter = JSONLogFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set log levels for specific loggers
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(log_level)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # Reduce SQL query logging


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.
    """
    return logging.getLogger(name)


class LoggerContextAdapter(logging.LoggerAdapter):
    """
    Logger adapter that adds context to log messages.
    """
    def __init__(self, logger: logging.Logger, extra: Optional[Dict[str, Any]] = None):
        super().__init__(logger, extra or {})
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        
        if self.extra:
            kwargs["extra"].update(self.extra)
        
        return msg, kwargs


def get_request_logger(request_id: str) -> LoggerContextAdapter:
    """
    Get a logger with request context.
    """
    logger = get_logger("app.request")
    return LoggerContextAdapter(logger, {"request_id": request_id})
