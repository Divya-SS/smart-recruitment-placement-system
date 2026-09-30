"""
Job & JobSkill Models Module.

Stores job postings, requirements, and required skill mappings.
"""

from app.extensions import db
from .base import BaseModel


class JobSkill(db.Model):
    """Junction table associating job requisitions with required skills."""
    __tablename__ = "job_skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(
        db.Integer, db.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_id = db.Column(
        db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    is_mandatory = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    job = db.relationship("Job", back_populates="skills")
    skill = db.relationship("Skill", back_populates="job_associations", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.name if self.skill else None,
            "category": self.skill.category if self.skill else None,
            "is_mandatory": self.is_mandatory
        }


class Job(BaseModel):
    """Stores job openings, requirements, and hiring constraints."""
    __tablename__ = "jobs"

    company_id = db.Column(
        db.Integer, db.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    assigned_recruiter_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    min_experience_years = db.Column(db.Numeric(4, 1), default=0.0, nullable=False)
    max_experience_years = db.Column(db.Numeric(4, 1), nullable=True)
    qualification_required = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=False, index=True)
    job_type = db.Column(
        db.Enum("FULL_TIME", "PART_TIME", "CONTRACT", "INTERNSHIP", name="job_type_enum"),
        default="FULL_TIME",
        nullable=False
    )
    min_salary = db.Column(db.Numeric(10, 2), nullable=True)
    max_salary = db.Column(db.Numeric(10, 2), nullable=True)
    openings_count = db.Column(db.Integer, default=1, nullable=False)
    status = db.Column(
        db.Enum("OPEN", "ON_HOLD", "CLOSED", name="job_status_enum"),
        default="OPEN",
        nullable=False,
        index=True
    )
    deadline = db.Column(db.Date, nullable=True)

    # Relationships
    company = db.relationship("Company", back_populates="jobs", lazy="joined")
    creator = db.relationship("User", foreign_keys=[created_by], back_populates="created_jobs", lazy="select")
    assigned_recruiter = db.relationship(
        "User", foreign_keys=[assigned_recruiter_id], back_populates="assigned_jobs", lazy="joined"
    )
    skills = db.relationship("JobSkill", back_populates="job", cascade="all, delete-orphan", lazy="selectin")
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "company_name": self.company.name if self.company else None,
            "assigned_recruiter_id": self.assigned_recruiter_id,
            "assigned_recruiter_name": self.assigned_recruiter.full_name if self.assigned_recruiter else None,
            "title": self.title,
            "description": self.description,
            "min_experience_years": float(self.min_experience_years) if self.min_experience_years is not None else 0.0,
            "max_experience_years": float(self.max_experience_years) if self.max_experience_years is not None else None,
            "qualification_required": self.qualification_required,
            "location": self.location,
            "job_type": self.job_type,
            "min_salary": float(self.min_salary) if self.min_salary is not None else None,
            "max_salary": float(self.max_salary) if self.max_salary is not None else None,
            "openings_count": self.openings_count,
            "status": self.status,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "skills": [s.to_dict() for s in self.skills] if self.skills else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Job id={self.id} title='{self.title}'>"
