"""
Matching Routes.

Endpoints for evaluating candidate-job compatibility and ranking candidates.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.matching_service import MatchingService
from app.utils.response import success_response

matching_bp = Blueprint("matching", __name__, url_prefix="/api/matching")


@matching_bp.route("/job/<int:job_id>", methods=["GET"])
@jwt_required()
def match_candidates_for_job(job_id):
    """Calculates compatibility scores for all candidates against a job."""
    min_score = float(request.args.get("min_score", 0.0))
    result = MatchingService.match_candidates_for_job(job_id, min_score=min_score)
    return success_response(data=result)


@matching_bp.route("/candidate/<int:candidate_id>", methods=["GET"])
@jwt_required()
def match_jobs_for_candidate(candidate_id):
    """Calculates compatibility scores for open jobs against a candidate."""
    min_score = float(request.args.get("min_score", 0.0))
    result = MatchingService.match_jobs_for_candidate(candidate_id, min_score=min_score)
    return success_response(data=result)
