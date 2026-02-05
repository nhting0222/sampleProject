import logging
import json
import sys
from datetime import datetime
from typing import Optional, Any
from functools import wraps
import time


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_obj["data"] = record.extra_data

        return json.dumps(log_obj)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Setup structured logging"""
    logger = logging.getLogger("xdr")
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers = []

    # Console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    return logger


# Create logger instance
logger = setup_logging()


class LoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that adds context to log messages"""

    def process(self, msg: str, kwargs: dict) -> tuple:
        extra = kwargs.get("extra", {})
        if self.extra:
            extra.update(self.extra)
        kwargs["extra"] = extra
        return msg, kwargs


def get_logger(name: str, **context) -> LoggerAdapter:
    """Get a logger with context"""
    base_logger = logging.getLogger(f"xdr.{name}")
    return LoggerAdapter(base_logger, context)


# Request logging decorator
def log_request(logger_name: str = "api"):
    """Decorator to log API requests"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            log = get_logger(logger_name)
            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000

                log.info(
                    f"{func.__name__} completed",
                    extra={
                        "extra_data": {
                            "function": func.__name__,
                            "duration_ms": round(duration, 2),
                            "status": "success"
                        }
                    }
                )
                return result

            except Exception as e:
                duration = (time.time() - start_time) * 1000

                log.error(
                    f"{func.__name__} failed: {str(e)}",
                    extra={
                        "extra_data": {
                            "function": func.__name__,
                            "duration_ms": round(duration, 2),
                            "status": "error",
                            "error": str(e)
                        }
                    }
                )
                raise

        return wrapper
    return decorator


# Audit logging
def log_audit(
    user_id: str,
    username: str,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None
):
    """Log audit event"""
    audit_logger = get_logger("audit")
    audit_logger.info(
        f"Audit: {username} {action} {resource_type}",
        extra={
            "extra_data": {
                "user_id": user_id,
                "username": username,
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "details": details,
                "ip_address": ip_address
            }
        }
    )


# Security logging
def log_security_event(
    event_type: str,
    severity: str,
    description: str,
    details: Optional[dict] = None
):
    """Log security event"""
    security_logger = get_logger("security")
    log_method = getattr(security_logger, severity.lower(), security_logger.info)
    log_method(
        f"Security: {event_type} - {description}",
        extra={
            "extra_data": {
                "event_type": event_type,
                "severity": severity,
                "description": description,
                "details": details
            }
        }
    )


# Performance metrics
class MetricsCollector:
    """Simple metrics collector"""

    def __init__(self):
        self.metrics = {
            "requests_total": 0,
            "requests_by_endpoint": {},
            "requests_by_status": {},
            "response_times": [],
            "errors_total": 0,
            "websocket_connections": 0
        }

    def record_request(self, endpoint: str, status: int, duration_ms: float):
        """Record a request"""
        self.metrics["requests_total"] += 1

        if endpoint not in self.metrics["requests_by_endpoint"]:
            self.metrics["requests_by_endpoint"][endpoint] = 0
        self.metrics["requests_by_endpoint"][endpoint] += 1

        status_group = f"{status // 100}xx"
        if status_group not in self.metrics["requests_by_status"]:
            self.metrics["requests_by_status"][status_group] = 0
        self.metrics["requests_by_status"][status_group] += 1

        # Keep last 1000 response times
        self.metrics["response_times"].append(duration_ms)
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]

        if status >= 500:
            self.metrics["errors_total"] += 1

    def record_websocket_connect(self):
        """Record WebSocket connection"""
        self.metrics["websocket_connections"] += 1

    def record_websocket_disconnect(self):
        """Record WebSocket disconnection"""
        self.metrics["websocket_connections"] = max(0, self.metrics["websocket_connections"] - 1)

    def get_metrics(self) -> dict:
        """Get current metrics"""
        response_times = self.metrics["response_times"]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return {
            "requests_total": self.metrics["requests_total"],
            "requests_by_endpoint": self.metrics["requests_by_endpoint"],
            "requests_by_status": self.metrics["requests_by_status"],
            "avg_response_time_ms": round(avg_response_time, 2),
            "errors_total": self.metrics["errors_total"],
            "websocket_connections": self.metrics["websocket_connections"]
        }

    def reset(self):
        """Reset metrics"""
        self.metrics = {
            "requests_total": 0,
            "requests_by_endpoint": {},
            "requests_by_status": {},
            "response_times": [],
            "errors_total": 0,
            "websocket_connections": self.metrics["websocket_connections"]  # Keep current connections
        }


# Global metrics collector
metrics = MetricsCollector()
