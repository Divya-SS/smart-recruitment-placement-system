"""
Application Model Module.

Tracks candidate pipeline progression through specific job postings.
"""

from app.extensions import db
from .base import BaseModel


class Application(BaseModel):
    __tablename__ = "applications"

    candidate_id = db.Column(
        db.Integer, db.ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id = db.Column(
        db.Integer, db.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    match_score = db.Column(db.Numeric(5, 2), default=0.00, nullable=False)
    status = db.Column(
        db.Enum(
            "APPLIED",
            "SHORTLISTED",
            "INTERVIEW_SCHEDULED",
            "SELECTED",
            "REJECTED",
            "JOINED",
            name="application_status_enum"
        ),
        default="APPLIED",
        nullable=False,
        index=True
    )
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    candidate = db.relationship("Candidate", back_populates="applications", lazy="joined")
    job = db.relationship("Job", back_populates="applications", lazy="joined")
    interviews = db.relationship("Interview", back_populates="application", cascade="all, delete-orphan", lazy="select")

    __table_args__ = (
        db.UniqueConstraint("candidate_id", "job_id", name="uq_candidate_job_application"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "candidate_name": self.candidate.full_name if self.candidate else None,
            "candidate_email": self.candidate.email if self.candidate else None,
            "job_id": self.job_id,
            "job_title": self.job.title if self.job else None,
            "company_name": self.job.company.name if self.job and self.job.company else None,
            "match_score": float(self.match_score) if self.match_score is not None else 0.0,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Application id={self.id} candidate_id={self.candidate_id} job_id={self.job_id} status='{self.status}'>"
