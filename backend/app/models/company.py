"""
Company Model Module.

Stores hiring partner companies and contact representatives.
"""

from app.extensions import db
from .base import BaseModel


class Company(BaseModel):
    __tablename__ = "companies"

    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    website = db.Column(db.String(150), nullable=True)
    industry = db.Column(db.String(80), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    contact_person_name = db.Column(db.String(100), nullable=False)
    contact_person_email = db.Column(db.String(120), nullable=False)
    contact_person_phone = db.Column(db.String(20), nullable=False)
    status = db.Column(
        db.Enum("ACTIVE", "INACTIVE", name="company_status_enum"),
        default="ACTIVE",
        nullable=False,
        index=True
    )

    # Relationships
    jobs = db.relationship("Job", back_populates="company", cascade="all, delete-orphan", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "website": self.website,
            "industry": self.industry,
            "location": self.location,
            "contact_person_name": self.contact_person_name,
            "contact_person_email": self.contact_person_email,
            "contact_person_phone": self.contact_person_phone,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Company id={self.id} name='{self.name}'>"
