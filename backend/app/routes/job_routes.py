"""
Job Routes.

Job posting management and skill requirement endpoints.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.job_service import JobService
from app.utils.response import success_response
from app.utils.decorators import admin_required

job_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")


@job_bp.route("", methods=["GET"])
@jwt_required()
def list_jobs():
    """List jobs with filters and search."""
    search = request.args.get("search")
    company_id = request.args.get("company_id")
    recruiter_id = request.args.get("recruiter_id")
    status = request.args.get("status")
    job_type = request.args.get("job_type")
    location = request.args.get("location")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))

    result = JobService.get_jobs(
        search=search,
        company_id=company_id,
        recruiter_id=recruiter_id,
        status=status,
        job_type=job_type,
        location=location,
        page=page,
        per_page=per_page
    )
    return success_response(data=result)


@job_bp.route("/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id):
    """Get single job details."""
    job = JobService.get_job_by_id(job_id)
    return success_response(data=job)


@job_bp.route("", methods=["POST"])
@jwt_required()
def create_job():
    """Create new job posting."""
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    job = JobService.create_job(data, created_by=int(user_id) if user_id else None)
    return success_response(message="Job created successfully", data=job, status_code=201)


@job_bp.route("/<int:job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    """Update job posting."""
    data = request.get_json() or {}
    job = JobService.update_job(job_id, data)
    return success_response(message="Job updated successfully", data=job)


@job_bp.route("/<int:job_id>", methods=["DELETE"])
@admin_required()
def delete_job(job_id):
    """Delete job posting (Admin only)."""
    result = JobService.delete_job(job_id)
    return success_response(message="Job deleted successfully", data=result)
