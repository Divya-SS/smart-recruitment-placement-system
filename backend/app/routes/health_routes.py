"""
Health Check Routes Module.

Provides service liveness and database connectivity status.
"""

from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Service Health Check Endpoint.

    Returns:
        JSON response with system status and message.
    """
    return jsonify({
        "status": "success",
        "message": "Smart Recruitment API is running"
    }), 200


@health_bp.route("/health/db", methods=["GET"])
def db_health_check():
    """
    Database Connectivity Health Check.

    Attempts a lightweight SELECT 1 query against the configured database.
    """
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({
            "status": "success",
            "message": "Database connection is healthy",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Database connection failed",
            "database": "disconnected",
            "detail": str(e)
        }), 503
