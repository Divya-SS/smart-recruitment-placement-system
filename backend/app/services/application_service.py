"""
Application Service.

Handles candidate pipeline progression through jobs, tracking status transitions.
"""

from sqlalchemy import or_
from app.extensions import db
from app.models import Application, Job, Candidate
from app.utils.exceptions import ResourceNotFoundError, ValidationError, ConflictError
from app.services.matching_service import MatchingService

ALLOWED_STATUSES = ["APPLIED", "SHORTLISTED", "INTERVIEW_SCHEDULED", "SELECTED", "REJECTED", "JOINED"]


class ApplicationService:
    @staticmethod
    def get_applications(job_id=None, candidate_id=None, status=None, search=None, page=1, per_page=50):
        """Fetches applications with multi-criteria filtering."""
        query = Application.query

        if job_id:
            query = query.filter(Application.job_id == int(job_id))

        if candidate_id:
            query = query.filter(Application.candidate_id == int(candidate_id))

        if status:
            query = query.filter(Application.status == status.upper())

        if search:
            search_term = f"%{search.strip()}%"
            query = query.join(Candidate).join(Job).filter(
                or_(
                    Candidate.first_name.ilike(search_term),
                    Candidate.last_name.ilike(search_term),
                    Candidate.email.ilike(search_term),
                    Job.title.ilike(search_term)
                )
            )

        query = query.order_by(Application.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [a.to_dict() for a in paginated.items],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages,
            "per_page": paginated.per_page
        }

    @staticmethod
    def get_application_by_id(application_id):
        """Retrieves single application with interview details."""
        app_record = db.session.get(Application, int(application_id))
        if not app_record:
            raise ResourceNotFoundError(f"Application ID {application_id} not found")
        data = app_record.to_dict()
        data["interviews"] = [i.to_dict() for i in app_record.interviews]
        return data

    @staticmethod
    def create_application(candidate_id, job_id, notes=None):
        """Maps candidate to job, calculates match score snapshot."""
        candidate = db.session.get(Candidate, int(candidate_id))
        if not candidate:
            raise ResourceNotFoundError(f"Candidate ID {candidate_id} not found")

        job = db.session.get(Job, int(job_id))
        if not job:
            raise ResourceNotFoundError(f"Job ID {job_id} not found")

        existing = Application.query.filter_by(candidate_id=candidate.id, job_id=job.id).first()
        if existing:
            raise ConflictError("Candidate has already applied to this job posting")

        # Compute match score snapshot
        match_result = MatchingService.calculate_match(job, candidate)
        score = match_result["total_match_score"]

        app_record = Application(
            candidate_id=candidate.id,
            job_id=job.id,
            match_score=score,
            status="APPLIED",
            notes=notes
        )
        db.session.add(app_record)
        db.session.commit()
        return app_record.to_dict()

    @staticmethod
    def update_status(application_id, new_status, notes=None):
        """Advances application lifecycle state."""
        app_record = db.session.get(Application, int(application_id))
        if not app_record:
            raise ResourceNotFoundError(f"Application ID {application_id} not found")

        status_clean = new_status.upper()
        if status_clean not in ALLOWED_STATUSES:
            raise ValidationError(f"Invalid status '{new_status}'. Must be one of {ALLOWED_STATUSES}")

        app_record.status = status_clean
        if notes:
            app_record.notes = notes

        # Update candidate state if placed
        if status_clean == "JOINED":
            app_record.candidate.status = "PLACED"
        elif status_clean in ["SHORTLISTED", "INTERVIEW_SCHEDULED"] and app_record.candidate.status == "AVAILABLE":
            app_record.candidate.status = "INTERVIEWING"

        db.session.commit()
        return app_record.to_dict()

    @staticmethod
    def delete_application(application_id):
        """Deletes an application record."""
        app_record = db.session.get(Application, int(application_id))
        if not app_record:
            raise ResourceNotFoundError(f"Application ID {application_id} not found")
        db.session.delete(app_record)
        db.session.commit()
        return {"deleted": True, "id": application_id}
