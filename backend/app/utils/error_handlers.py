"""
Global Error Handlers.

Catches standard HTTP errors, custom application exceptions, SQLAlchemy integrity
errors, and unhandled 500 exceptions, returning uniform JSON envelopes.
"""

import logging
from flask import jsonify
from sqlalchemy.exc import IntegrityError, OperationalError
from .exceptions import AppException

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Registers all global error handlers onto the Flask application instance."""

    @app.errorhandler(AppException)
    def handle_app_exception(error):
        """Catches custom domain AppException and derivatives."""
        response = {
            "status": "error",
            "message": error.message,
            "data": None,
            "errors": error.errors
        }
        return jsonify(response), error.status_code

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({
            "status": "error",
            "message": "Bad request",
            "data": None,
            "errors": str(error.description) if hasattr(error, 'description') else None
        }), 400

    @app.errorhandler(401)
    def handle_unauthorized(error):
        return jsonify({
            "status": "error",
            "message": "Unauthorized access",
            "data": None,
            "errors": None
        }), 401

    @app.errorhandler(403)
    def handle_forbidden(error):
        return jsonify({
            "status": "error",
            "message": "Forbidden: You do not have permission to perform this action",
            "data": None,
            "errors": None
        }), 403

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "status": "error",
            "message": "The requested API endpoint or resource was not found",
            "data": None,
            "errors": None
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({
            "status": "error",
            "message": "HTTP Method Not Allowed for this endpoint",
            "data": None,
            "errors": None
        }), 405

    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        """Catches Marshmallow validation or unprocessable entity errors."""
        messages = getattr(error, 'data', {}).get('messages', str(error))
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "data": None,
            "errors": messages
        }), 422

    @app.errorhandler(IntegrityError)
    def handle_db_integrity_error(error):
        """Catches database constraint violations (duplicate keys, FK violations)."""
        logger.error(f"Database IntegrityError: {error}")
        return jsonify({
            "status": "error",
            "message": "Database constraint violation. A record with these details may already exist.",
            "data": None,
            "errors": None
        }), 409

    @app.errorhandler(OperationalError)
    def handle_db_operational_error(error):
        """Catches database connectivity errors without leaking sensitive stack traces."""
        logger.error(f"Database OperationalError: {error}")
        return jsonify({
            "status": "error",
            "message": "Database service is temporarily unavailable. Please verify connectivity.",
            "data": None,
            "errors": None
        }), 503

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """Catches all unhandled server exceptions."""
        logger.error(f"Internal Server Error: {error}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "An internal server error occurred. Please try again later.",
            "data": None,
            "errors": None
        }), 500
