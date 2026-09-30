"""
Interview & InterviewFeedback Models Module.

Tracks interview schedules, rounds, and evaluation scores.
"""

from datetime import datetime, timezone
from app.extensions import db
from .base import BaseModel


class Interview(BaseModel):
    __tablename__ = "interviews"

    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scheduled_by = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    interview_round = db.Column(db.String(60), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False, index=True)
    mode = db.Column(
        db.Enum("ONLINE", "IN_PERSON", "TELEPHONIC", name="interview_mode_enum"),
        default="ONLINE",
        nullable=False
    )
    meeting_link_or_venue = db.Column(db.String(255), nullable=True)
    interviewer_name = db.Column(db.String(100), nullable=False)
    interviewer_email = db.Column(db.String(120), nullable=True)
    status = db.Column(
        db.Enum("SCHEDULED", "COMPLETED", "CANCELLED", "RESCHEDULED", name="interview_status_enum"),
        default="SCHEDULED",
        nullable=False,
        index=True
    )

    # Relationships
    application = db.relationship("Application", back_populates="interviews", lazy="joined")
    scheduler = db.relationship("User", back_populates="scheduled_interviews", lazy="select")
    feedback = db.relationship(
        "InterviewFeedback", back_populates="interview", uselist=False, cascade="all, delete-orphan", lazy="joined"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "candidate_name": self.application.candidate.full_name if self.application and self.application.candidate else None,
            "job_title": self.application.job.title if self.application and self.application.job else None,
            "interview_round": self.interview_round,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "mode": self.mode,
            "meeting_link_or_venue": self.meeting_link_or_venue,
            "interviewer_name": self.interviewer_name,
            "interviewer_email": self.interviewer_email,
            "status": self.status,
            "scheduled_by": self.scheduled_by,
            "feedback": self.feedback.to_dict() if self.feedback else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<Interview id={self.id} round='{self.interview_round}' status='{self.status}'>"


class InterviewFeedback(db.Model):
    __tablename__ = "interview_feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(
        db.Integer, db.ForeignKey("interviews.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    technical_rating = db.Column(db.Integer, nullable=False)
    communication_rating = db.Column(db.Integer, nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    recommendation = db.Column(
        db.Enum("STRONG_HIRE", "HIRE", "HOLD", "NO_HIRE", name="feedback_recommendation_enum"),
        nullable=False
    )
    submitted_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    interview = db.relationship("Interview", back_populates="feedback")

    __table_args__ = (
        db.CheckConstraint("technical_rating >= 1 AND technical_rating <= 5", name="chk_tech_rating_range"),
        db.CheckConstraint("communication_rating >= 1 AND communication_rating <= 5", name="chk_comm_rating_range"),
        db.CheckConstraint("overall_rating >= 1 AND overall_rating <= 5", name="chk_overall_rating_range"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "technical_rating": self.technical_rating,
            "communication_rating": self.communication_rating,
            "overall_rating": self.overall_rating,
            "comments": self.comments,
            "recommendation": self.recommendation,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None
        }

    def __repr__(self):
        return f"<InterviewFeedback interview_id={self.interview_id} rating={self.overall_rating}>"
