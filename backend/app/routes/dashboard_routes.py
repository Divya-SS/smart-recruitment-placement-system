"""
Dashboard Analytics Routes.

Provides endpoints for KPIs, pipeline metrics, and charts.
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.services.dashboard_service import DashboardService
from app.utils.response import success_response

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/metrics", methods=["GET"])
@jwt_required()
def get_metrics():
    """Get high-level summary KPIs."""
    metrics = DashboardService.get_summary_metrics()
    return success_response(data=metrics)


@dashboard_bp.route("/pipeline", methods=["GET"])
@jwt_required()
def get_pipeline():
    """Get application pipeline stage counts."""
    funnel = DashboardService.get_pipeline_funnel()
    return success_response(data=funnel)


@dashboard_bp.route("/recent-interviews", methods=["GET"])
@jwt_required()
def get_recent_interviews():
    """Get upcoming interviews list."""
    interviews = DashboardService.get_recent_interviews(limit=5)
    return success_response(data=interviews)
