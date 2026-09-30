"""
Candidate Routes.

CRUD and search endpoints for candidate profiles.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.candidate_service import CandidateService
from app.utils.response import success_response
from app.utils.decorators import recruiter_or_admin_required, admin_required

candidate_bp = Blueprint("candidates", __name__, url_prefix="/api/candidates")


@candidate_bp.route("", methods=["GET"])
@jwt_required()
def list_candidates():
    """List candidates with query filters."""
    search = request.args.get("search")
    skill = request.args.get("skill")
    location = request.args.get("location")
    min_exp = request.args.get("min_exp")
    max_exp = request.args.get("max_exp")
    status = request.args.get("status")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))

    result = CandidateService.get_candidates(
        search=search,
        skill=skill,
        location=location,
        min_exp=min_exp,
        max_exp=max_exp,
        status=status,
        page=page,
        per_page=per_page
    )
    return success_response(data=result)


@candidate_bp.route("/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_candidate(candidate_id):
    """Get single candidate by ID."""
    candidate = CandidateService.get_candidate_by_id(candidate_id)
    return success_response(data=candidate)


@candidate_bp.route("", methods=["POST"])
@jwt_required()
def create_candidate():
    """Create new candidate profile."""
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    new_cand = CandidateService.create_candidate(data, created_by=int(user_id) if user_id else None)
    return success_response(message="Candidate created successfully", data=new_cand, status_code=201)


@candidate_bp.route("/<int:candidate_id>", methods=["PUT"])
@jwt_required()
def update_candidate(candidate_id):
    """Update candidate profile."""
    data = request.get_json() or {}
    updated = CandidateService.update_candidate(candidate_id, data)
    return success_response(message="Candidate updated successfully", data=updated)


@candidate_bp.route("/<int:candidate_id>", methods=["DELETE"])
@admin_required()
def delete_candidate(candidate_id):
    """Delete candidate profile (Admin only)."""
    result = CandidateService.delete_candidate(candidate_id)
    return success_response(message="Candidate deleted successfully", data=result)


@candidate_bp.route("/skills", methods=["GET"])
@jwt_required()
def list_skills():
    """Get list of available skills in catalog."""
    skills = CandidateService.get_all_skills()
    return success_response(data=skills)
