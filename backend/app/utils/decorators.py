"""
Authorization Decorators.

Provides reusable decorators for role-based access control (RBAC).
"""

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from .exceptions import AuthorizationError, AuthenticationError


def role_required(allowed_roles):
    """
    Decorator to restrict endpoint access to specific roles.

    :param allowed_roles: List of allowed role names (e.g. ['ADMIN', 'RECRUITER']) or single string
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    # Normalize roles to uppercase
    allowed_roles = [r.upper() for r in allowed_roles]

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as e:
                raise AuthenticationError(str(e))

            claims = get_jwt()
            user_role = claims.get("role", "").upper()

            if user_role not in allowed_roles:
                raise AuthorizationError(
                    f"Access forbidden: User with role '{user_role}' cannot access this resource"
                )

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required():
    """Convenience decorator for admin-only endpoints."""
    return role_required(["ADMIN"])


def recruiter_or_admin_required():
    """Convenience decorator for recruiter and admin accessible endpoints."""
    return role_required(["ADMIN", "RECRUITER"])
