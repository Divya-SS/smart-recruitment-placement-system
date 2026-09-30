"""
Custom Application Exceptions.

Defines hierarchy of domain-specific exceptions with HTTP status mappings.
"""


class AppException(Exception):
    """Base exception for all domain-specific application errors."""
    status_code = 500
    message = "An unexpected error occurred"

    def __init__(self, message=None, status_code=None, errors=None):
        super().__init__(message or self.message)
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        self.errors = errors

    def to_dict(self):
        return {
            "status": "error",
            "message": self.message,
            "errors": self.errors
        }


class ValidationError(AppException):
    """Raised when client input fails business or schema validation."""
    status_code = 400
    message = "Validation error"


class AuthenticationError(AppException):
    """Raised when credentials or tokens are invalid/missing."""
    status_code = 401
    message = "Authentication required"


class AuthorizationError(AppException):
    """Raised when user lacks permissions for an action."""
    status_code = 403
    message = "Access forbidden: insufficient permissions"


class ResourceNotFoundError(AppException):
    """Raised when a requested resource does not exist."""
    status_code = 404
    message = "Resource not found"


class ConflictError(AppException):
    """Raised when an operation conflicts with current state (e.g. duplicate key)."""
    status_code = 409
    message = "Resource conflict"
