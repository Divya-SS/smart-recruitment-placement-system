"""
Authentication Routes.

Handles user login, token refresh, and profile retrieval.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticates user credentials."""
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    auth_data = AuthService.authenticate(email, password)
    return success_response(message="Login successful", data=auth_data)


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Retrieves profile of the authenticated user."""
    user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(user_id)
    return success_response(data=user)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """Generates new access token from refresh token."""
    user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(user_id)
    
    from flask_jwt_extended import create_access_token
    additional_claims = {
        "role": user.get("role_name", "RECRUITER"),
        "name": user.get("full_name"),
        "email": user.get("email")
    }
    new_access_token = create_access_token(identity=str(user["id"]), additional_claims=additional_claims)
    return success_response(data={"access_token": new_access_token})
