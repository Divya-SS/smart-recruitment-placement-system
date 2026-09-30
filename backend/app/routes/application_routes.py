"""
Application Routes.

Endpoints for managing job applications and lifecycle progression.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.application_service import ApplicationService
from app.utils.response import success_response
from app.utils.decorators import admin_required

application_bp = Blueprint("applications", __name__, url_prefix="/api/applications")


@application_bp.route("", methods=["GET"])
@jwt_required()
def list_applications():
    """List applications with filters."""
    job_id = request.args.get("job_id")
    candidate_id = request.args.get("candidate_id")
    status = request.args.get("status")
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))

    result = ApplicationService.get_applications(
        job_id=job_id,
        candidate_id=candidate_id,
        status=status,
        search=search,
        page=page,
        per_page=per_page
    )
    return success_response(data=result)


@application_bp.route("/<int:application_id>", methods=["GET"])
@jwt_required()
def get_application(application_id):
    """Get single application details."""
    app_record = ApplicationService.get_application_by_id(application_id)
    return success_response(data=app_record)


@application_bp.route("", methods=["POST"])
@jwt_required()
def create_application():
    """Map candidate to job."""
    data = request.get_json() or {}
    candidate_id = data.get("candidate_id")
    job_id = data.get("job_id")
    notes = data.get("notes")

    app_record = ApplicationService.create_application(candidate_id, job_id, notes=notes)
    return success_response(message="Application created successfully", data=app_record, status_code=201)


@application_bp.route("/<int:application_id>/status", methods=["PATCH"])
@jwt_required()
def update_application_status(application_id):
    """Advance application status."""
    data = request.get_json() or {}
    new_status = data.get("status")
    notes = data.get("notes")

    updated = ApplicationService.update_status(application_id, new_status, notes=notes)
    return success_response(message="Application status updated", data=updated)


@application_bp.route("/<int:application_id>", methods=["DELETE"])
@admin_required()
def delete_application(application_id):
    """Delete application record."""
    result = ApplicationService.delete_application(application_id)
    return success_response(message="Application deleted successfully", data=result)
