"""
Candidate & CandidateSkill Models Module.

Stores candidate profiles and their associated technical skills.
"""

from app.extensions import db
from .base import BaseModel


class CandidateSkill(db.Model):
    """Junction table associating candidates with skills and proficiency level."""
    __tablename__ = "candidate_skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidate_id = db.Column(
        db.Integer, db.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_id = db.Column(
        db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    proficiency = db.Column(
        db.Enum("BEGINNER", "INTERMEDIATE", "EXPERT", name="proficiency_enum"),
        default="INTERMEDIATE",
        nullable=False
    )

    # Relationships
    candidate = db.relationship("Candidate", back_populates="skills")
    skill = db.relationship("Skill", back_populates="candidate_associations", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("candidate_id", "skill_id", name="uq_candidate_skill"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.name if self.skill else None,
            "category": self.skill.category if self.skill else None,
            "proficiency": self.proficiency
        }


class Candidate(BaseModel):
    """Stores candidate profile and career metadata."""
    __tablename__ = "candidates"

    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False, index=True)
    experience_years = db.Column(db.Numeric(4, 1), default=0.0, nullable=False)
    highest_qualification = db.Column(db.String(100), nullable=False)
    current_company = db.Column(db.String(120), nullable=True)
    current_ctc = db.Column(db.Numeric(10, 2), nullable=True)
    expected_ctc = db.Column(db.Numeric(10, 2), nullable=True)
    resume_url = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.Enum("AVAILABLE", "SHORTLISTED", "INTERVIEWING", "PLACED", "INACTIVE", name="candidate_status_enum"),
        default="AVAILABLE",
        nullable=False,
        index=True
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    creator = db.relationship("User", back_populates="created_candidates", lazy="select")
    skills = db.relationship("CandidateSkill", back_populates="candidate", cascade="all, delete-orphan", lazy="selectin")
    applications = db.relationship("Application", back_populates="candidate", cascade="all, delete-orphan", lazy="select")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "experience_years": float(self.experience_years) if self.experience_years is not None else 0.0,
            "highest_qualification": self.highest_qualification,
            "current_company": self.current_company,
            "current_ctc": float(self.current_ctc) if self.current_ctc is not None else None,
            "expected_ctc": float(self.expected_ctc) if self.expected_ctc is not None else None,
            "resume_url": self.resume_url,
            "status": self.status,
            "created_by": self.created_by,
            "skills": [s.to_dict() for s in self.skills] if self.skills else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Candidate id={self.id} email='{self.email}'>"
