from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Callable

from ..core.logging import logger, metrics, get_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and collecting metrics"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timing
        start_time = time.time()

        # Get request info
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"

        # Create request logger
        request_logger = get_logger(
            "request",
            method=method,
            path=path,
            client_ip=client_ip
        )

        # Log request start
        request_logger.info(f"Request started: {method} {path}")

        # Process request
        try:
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000

            # Record metrics
            metrics.record_request(path, response.status_code, duration_ms)

            # Log request completion
            request_logger.info(
                f"Request completed: {method} {path}",
                extra={
                    "extra_data": {
                        "status_code": response.status_code,
                        "duration_ms": round(duration_ms, 2)
                    }
                }
            )

            # Add timing header
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

            return response

        except Exception as e:
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000

            # Record error metrics
            metrics.record_request(path, 500, duration_ms)

            # Log error
            request_logger.error(
                f"Request failed: {method} {path}",
                extra={
                    "extra_data": {
                        "error": str(e),
                        "duration_ms": round(duration_ms, 2)
                    }
                },
                exc_info=True
            )

            raise
