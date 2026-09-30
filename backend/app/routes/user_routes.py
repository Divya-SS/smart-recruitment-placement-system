"""
User Management Routes (Admin Only).

Endpoints for inviting recruiters, listing staff accounts, and toggling status.
"""

from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.utils.response import success_response
from app.utils.decorators import admin_required

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.route("", methods=["GET"])
@admin_required()
def list_users():
    """List all team accounts."""
    users = AuthService.list_users()
    return success_response(data=users)


@user_bp.route("", methods=["POST"])
@admin_required()
def create_user():
    """Create new user account."""
    data = request.get_json() or {}
    user = AuthService.create_user(
        full_name=data.get("full_name"),
        email=data.get("email"),
        password=data.get("password"),
        role_name=data.get("role_name", "RECRUITER"),
        phone=data.get("phone")
    )
    return success_response(message="User created successfully", data=user, status_code=201)


@user_bp.route("/<int:user_id>/toggle-status", methods=["PATCH"])
@admin_required()
def toggle_user_status(user_id):
    """Toggle user active status."""
    user = AuthService.toggle_user_status(user_id)
    return success_response(message="User status updated", data=user)
