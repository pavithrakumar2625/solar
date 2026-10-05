"""
SolarRecover AI — Application Exceptions
Structured error handling with consistent API error responses.
"""
from typing import Any

from fastapi import HTTPException, status


class SolarRecoverError(Exception):
    """Base exception for all SolarRecover AI errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(SolarRecoverError):
    """Resource not found."""
    pass


class ConflictError(SolarRecoverError):
    """Resource conflict (e.g., duplicate)."""
    pass


class ValidationError(SolarRecoverError):
    """Input validation failed."""
    pass


class AuthenticationError(SolarRecoverError):
    """Authentication failed."""
    pass


class AuthorizationError(SolarRecoverError):
    """Authorization/permission denied."""
    pass


class TenantIsolationError(SolarRecoverError):
    """Cross-organization access attempt."""
    pass


class DataQualityError(SolarRecoverError):
    """Data quality check failed."""
    pass


class ModelError(SolarRecoverError):
    """ML model error."""
    pass


class ExternalServiceError(SolarRecoverError):
    """External service (weather API, LLM, etc.) failure."""
    pass


class JobError(SolarRecoverError):
    """Background job error."""
    pass


# HTTP exception helpers
def http_404(detail: str = "Resource not found") -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def http_400(detail: str = "Bad request") -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def http_401(detail: str = "Not authenticated") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def http_403(detail: str = "Permission denied") -> HTTPException:
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def http_409(detail: str = "Conflict") -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def http_422(detail: str = "Validation error") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
    )


def http_500(detail: str = "Internal server error") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
    )


def http_503(detail: str = "Service unavailable") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail
    )
