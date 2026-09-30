"""
Authentication Service.

Handles user credential verification, JWT issuance, and user onboarding.
"""

from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db
from app.models import User, Role
from app.utils.exceptions import AuthenticationError, ConflictError, ResourceNotFoundError, ValidationError


class AuthService:
    @staticmethod
    def authenticate(email, password):
        """Authenticates user credentials and returns tokens and user profile."""
        if not email or not password:
            raise ValidationError("Email and password are required")

        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user or not user.check_password(password):
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            raise AuthenticationError("This account has been deactivated. Please contact an administrator.")

        # Additional claims stored in JWT
        additional_claims = {
            "role": user.role.name if user.role else "RECRUITER",
            "name": user.full_name,
            "email": user.email
        }

        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

        return {
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @staticmethod
    def get_user_by_id(user_id):
        """Fetches user profile by ID."""
        user = db.session.get(User, int(user_id))
        if not user:
            raise ResourceNotFoundError("User not found")
        return user.to_dict()

    @staticmethod
    def create_user(full_name, email, password, role_name="RECRUITER", phone=None):
        """Creates a new user account (Admin privilege)."""
        if not full_name or not email or not password:
            raise ValidationError("Full name, email, and password are required")

        email_clean = email.strip().lower()
        if User.query.filter_by(email=email_clean).first():
            raise ConflictError(f"User with email '{email_clean}' already exists")

        role = Role.query.filter_by(name=role_name.upper()).first()
        if not role:
            raise ValidationError(f"Invalid role '{role_name}'")

        new_user = User(
            role_id=role.id,
            full_name=full_name.strip(),
            email=email_clean,
            phone=phone.strip() if phone else None,
            is_active=True
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return new_user.to_dict()

    @staticmethod
    def list_users():
        """Lists all system users."""
        users = User.query.order_by(User.created_at.desc()).all()
        return [u.to_dict() for u in users]

    @staticmethod
    def toggle_user_status(user_id):
        """Activates or deactivates a user account."""
        user = db.session.get(User, int(user_id))
        if not user:
            raise ResourceNotFoundError("User not found")
        user.is_active = not user.is_active
        db.session.commit()
        return user.to_dict()
