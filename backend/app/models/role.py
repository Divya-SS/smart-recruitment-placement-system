"""
Role Model Module.

Stores user authorization roles (e.g. ADMIN, RECRUITER).
"""

from datetime import datetime, timezone
from app.extensions import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False, index=True)
    description = db.Column(db.String(150), nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    users = db.relationship("User", back_populates="role", cascade="all, delete-orphan", lazy="select")

    def __repr__(self):
        return f"<Role id={self.id} name='{self.name}'>"
