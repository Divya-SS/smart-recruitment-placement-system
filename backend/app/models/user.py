"""
User Model Module.

Stores accounts for Admins and Recruiters with Bcrypt password hashing.
"""

import bcrypt
from app.extensions import db
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    role = db.relationship("Role", back_populates="users", lazy="joined")
    created_jobs = db.relationship("Job", foreign_keys="Job.created_by", back_populates="creator", lazy="select")
    assigned_jobs = db.relationship("Job", foreign_keys="Job.assigned_recruiter_id", back_populates="assigned_recruiter", lazy="select")
    created_candidates = db.relationship("Candidate", back_populates="creator", lazy="select")
    scheduled_interviews = db.relationship("Interview", back_populates="scheduler", lazy="select")

    def set_password(self, password: str) -> None:
        """Hashes plaintext password with bcrypt salt."""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verifies candidate plaintext password against stored bcrypt hash."""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def to_dict(self):
        """Converts user instance to safe dictionary without password_hash."""
        return {
            "id": self.id,
            "role_id": self.role_id,
            "role_name": self.role.name if self.role else None,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<User id={self.id} email='{self.email}'>"
