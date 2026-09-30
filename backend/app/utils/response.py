"""
Standardized API Response Builder.

Ensures consistent JSON response format across all endpoints:
{
    "status": "success" | "error" | "fail",
    "message": "Human-readable description",
    "data": { ... } | null,
    "errors": { ... } | null
}
"""

from flask import jsonify


def api_response(status="success", message="", data=None, errors=None, status_code=200):
    """
    Builds a structured JSON response.

    :param status: "success", "error", or "fail"
    :param message: Human-readable status message
    :param data: Payload data (dict, list, or primitive)
    :param errors: Validation or field-specific error details
    :param status_code: HTTP status code
    :return: Flask JSON response object with status code
    """
    payload = {
        "status": status,
        "message": message,
        "data": data,
        "errors": errors
    }
    return jsonify(payload), status_code


def success_response(message="Operation successful", data=None, status_code=200):
    """Convenience wrapper for successful API responses."""
    return api_response(
        status="success",
        message=message,
        data=data,
        errors=None,
        status_code=status_code
    )


def error_response(message="An error occurred", errors=None, status_code=400):
    """Convenience wrapper for error API responses."""
    return api_response(
        status="error",
        message=message,
        data=None,
        errors=errors,
        status_code=status_code
    )
