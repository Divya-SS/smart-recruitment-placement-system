"""
Interview Routes.

Endpoints for interview scheduling and evaluation feedback.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.interview_service import InterviewService
from app.utils.response import success_response
from app.utils.decorators import admin_required

interview_bp = Blueprint("interviews", __name__, url_prefix="/api/interviews")


@interview_bp.route("", methods=["GET"])
@jwt_required()
def list_interviews():
    """List interviews with filters."""
    status = request.args.get("status")
    application_id = request.args.get("application_id")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))

    result = InterviewService.get_interviews(
        status=status,
        application_id=application_id,
        page=page,
        per_page=per_page
    )
    return success_response(data=result)


@interview_bp.route("/<int:interview_id>", methods=["GET"])
@jwt_required()
def get_interview(interview_id):
    """Get single interview details."""
    interview = InterviewService.get_interview_by_id(interview_id)
    return success_response(data=interview)


@interview_bp.route("", methods=["POST"])
@jwt_required()
def schedule_interview():
    """Schedule a new interview round."""
    data = request.get_json() or {}
    user_id = get_jwt_identity()
    interview = InterviewService.schedule_interview(data, scheduled_by=int(user_id) if user_id else None)
    return success_response(message="Interview scheduled successfully", data=interview, status_code=201)


@interview_bp.route("/<int:interview_id>", methods=["PUT"])
@jwt_required()
def update_interview(interview_id):
    """Update interview details."""
    data = request.get_json() or {}
    interview = InterviewService.update_interview(interview_id, data)
    return success_response(message="Interview updated successfully", data=interview)


@interview_bp.route("/<int:interview_id>/feedback", methods=["POST"])
@jwt_required()
def submit_feedback(interview_id):
    """Submit interview ratings and recommendation."""
    data = request.get_json() or {}
    interview = InterviewService.submit_feedback(interview_id, data)
    return success_response(message="Interview feedback submitted successfully", data=interview)


@interview_bp.route("/<int:interview_id>", methods=["DELETE"])
@admin_required()
def delete_interview(interview_id):
    """Delete interview record."""
    result = InterviewService.delete_interview(interview_id)
    return success_response(message="Interview deleted successfully", data=result)
