"""
Interview Service.

Handles interview scheduling, feedback recording, and candidate evaluation.
"""

from datetime import datetime
from app.extensions import db
from app.models import Interview, InterviewFeedback, Application
from app.utils.exceptions import ResourceNotFoundError, ValidationError, ConflictError


class InterviewService:
    @staticmethod
    def get_interviews(status=None, application_id=None, page=1, per_page=50):
        """Fetches interviews with status filtering."""
        query = Interview.query

        if status:
            query = query.filter(Interview.status == status.upper())

        if application_id:
            query = query.filter(Interview.application_id == int(application_id))

        query = query.order_by(Interview.scheduled_at.asc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [i.to_dict() for i in paginated.items],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages,
            "per_page": paginated.per_page
        }

    @staticmethod
    def get_interview_by_id(interview_id):
        """Retrieves interview details with feedback."""
        interview = db.session.get(Interview, int(interview_id))
        if not interview:
            raise ResourceNotFoundError(f"Interview ID {interview_id} not found")
        return interview.to_dict()

    @staticmethod
    def schedule_interview(data, scheduled_by=None):
        """Schedules a new interview round."""
        required = ["application_id", "interview_round", "scheduled_at", "interviewer_name"]
        for field in required:
            if not data.get(field):
                raise ValidationError(f"Field '{field}' is required")

        app_record = db.session.get(Application, int(data["application_id"]))
        if not app_record:
            raise ResourceNotFoundError(f"Application ID {data['application_id']} not found")

        try:
            scheduled_dt = datetime.fromisoformat(data["scheduled_at"].replace("Z", "+00:00"))
        except Exception:
            raise ValidationError("Invalid date format for 'scheduled_at'. Use ISO format (YYYY-MM-DDTHH:MM:SS)")

        interview = Interview(
            application_id=app_record.id,
            scheduled_by=scheduled_by,
            interview_round=data["interview_round"].strip(),
            scheduled_at=scheduled_dt,
            mode=data.get("mode", "ONLINE").upper(),
            meeting_link_or_venue=data.get("meeting_link_or_venue"),
            interviewer_name=data["interviewer_name"].strip(),
            interviewer_email=data.get("interviewer_email"),
            status="SCHEDULED"
        )
        db.session.add(interview)

        # Update application state
        app_record.status = "INTERVIEW_SCHEDULED"
        if app_record.candidate.status == "AVAILABLE":
            app_record.candidate.status = "INTERVIEWING"

        db.session.commit()
        return interview.to_dict()

    @staticmethod
    def update_interview(interview_id, data):
        """Updates interview details or reschedules."""
        interview = db.session.get(Interview, int(interview_id))
        if not interview:
            raise ResourceNotFoundError(f"Interview ID {interview_id} not found")

        for field in ["interview_round", "mode", "meeting_link_or_venue", "interviewer_name", "interviewer_email"]:
            if field in data and data[field] is not None:
                setattr(interview, field, str(data[field]).strip())

        if "scheduled_at" in data and data["scheduled_at"]:
            try:
                interview.scheduled_at = datetime.fromisoformat(data["scheduled_at"].replace("Z", "+00:00"))
            except Exception:
                raise ValidationError("Invalid date format for 'scheduled_at'")

        if "status" in data and data["status"]:
            interview.status = data["status"].upper()

        db.session.commit()
        return interview.to_dict()

    @staticmethod
    def submit_feedback(interview_id, data):
        """Records evaluation ratings and hiring recommendation."""
        interview = db.session.get(Interview, int(interview_id))
        if not interview:
            raise ResourceNotFoundError(f"Interview ID {interview_id} not found")

        required = ["technical_rating", "communication_rating", "overall_rating", "recommendation"]
        for field in required:
            if data.get(field) is None:
                raise ValidationError(f"Field '{field}' is required")

        for r_field in ["technical_rating", "communication_rating", "overall_rating"]:
            val = int(data[r_field])
            if val < 1 or val > 5:
                raise ValidationError(f"Rating '{r_field}' must be between 1 and 5")

        rec = data["recommendation"].upper()
        if rec not in ["STRONG_HIRE", "HIRE", "HOLD", "NO_HIRE"]:
            raise ValidationError("Recommendation must be STRONG_HIRE, HIRE, HOLD, or NO_HIRE")

        if interview.feedback:
            # Update existing
            interview.feedback.technical_rating = int(data["technical_rating"])
            interview.feedback.communication_rating = int(data["communication_rating"])
            interview.feedback.overall_rating = int(data["overall_rating"])
            interview.feedback.comments = data.get("comments")
            interview.feedback.recommendation = rec
        else:
            feedback = InterviewFeedback(
                interview_id=interview.id,
                technical_rating=int(data["technical_rating"]),
                communication_rating=int(data["communication_rating"]),
                overall_rating=int(data["overall_rating"]),
                comments=data.get("comments"),
                recommendation=rec
            )
            db.session.add(feedback)

        interview.status = "COMPLETED"
        db.session.commit()
        return interview.to_dict()

    @staticmethod
    def delete_interview(interview_id):
        """Deletes an interview record."""
        interview = db.session.get(Interview, int(interview_id))
        if not interview:
            raise ResourceNotFoundError(f"Interview ID {interview_id} not found")
        db.session.delete(interview)
        db.session.commit()
        return {"deleted": True, "id": interview_id}
