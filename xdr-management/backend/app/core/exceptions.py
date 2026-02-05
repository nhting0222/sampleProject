from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ErrorDetail(BaseModel):
    """Standard error detail schema"""
    code: str
    message: str
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response schema"""
    success: bool = False
    error: ErrorDetail
    timestamp: str


class AppException(Exception):
    """Base application exception"""
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[dict] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


# Specific exception classes
class NotFoundException(AppException):
    """Resource not found exception"""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            code=f"{resource.upper()}_NOT_FOUND",
            message=f"{resource} with ID '{resource_id}' not found",
            status_code=404,
            details={"resource": resource, "id": resource_id}
        )


class UnauthorizedException(AppException):
    """Unauthorized access exception"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=401
        )


class ForbiddenException(AppException):
    """Forbidden access exception"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=403
        )


class ValidationException(AppException):
    """Validation error exception"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details
        )


class ConflictException(AppException):
    """Conflict exception"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            code="CONFLICT",
            message=message,
            status_code=409,
            details=details
        )


class InternalServerException(AppException):
    """Internal server error exception"""
    def __init__(self, message: str = "An unexpected error occurred"):
        super().__init__(
            code="INTERNAL_SERVER_ERROR",
            message=message,
            status_code=500
        )


def create_error_response(exception: AppException) -> JSONResponse:
    """Create standard error response from exception"""
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "success": False,
            "error": {
                "code": exception.code,
                "message": exception.message,
                "details": exception.details
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Global exception handler for AppException"""
    return create_error_response(exc)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Global exception handler for HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "details": None
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": None
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )
