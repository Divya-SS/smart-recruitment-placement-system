"""
Dashboard Analytics Service.

Provides aggregated KPIs, recruitment pipeline funnel counts, and placement metrics.
"""

from sqlalchemy import func
from app.extensions import db
from app.models import Candidate, Job, Company, Application, Interview


class DashboardService:
    @staticmethod
    def get_summary_metrics():
        """Aggregates high-level system KPIs."""
        total_candidates = Candidate.query.count()
        active_jobs = Job.query.filter_by(status="OPEN").count()
        total_companies = Company.query.filter_by(status="ACTIVE").count()
        total_applications = Application.query.count()
        interviews_scheduled = Interview.query.filter_by(status="SCHEDULED").count()
        placed_candidates = Candidate.query.filter_by(status="PLACED").count()
        shortlisted_candidates = Application.query.filter_by(status="SHORTLISTED").count()

        return {
            "total_candidates": total_candidates,
            "active_jobs": active_jobs,
            "total_companies": total_companies,
            "total_applications": total_applications,
            "interviews_scheduled": interviews_scheduled,
            "placed_candidates": placed_candidates,
            "shortlisted_candidates": shortlisted_candidates
        }

    @staticmethod
    def get_pipeline_funnel():
        """Calculates candidate distribution across all application stages."""
        stages = [
            ("APPLIED", "Applied"),
            ("SHORTLISTED", "Shortlisted"),
            ("INTERVIEW_SCHEDULED", "Interview Scheduled"),
            ("SELECTED", "Selected"),
            ("REJECTED", "Rejected"),
            ("JOINED", "Joined / Placed")
        ]

        funnel_data = []
        for code, label in stages:
            count = Application.query.filter_by(status=code).count()
            funnel_data.append({
                "stage": code,
                "label": label,
                "count": count
            })

        return funnel_data

    @staticmethod
    def get_recent_interviews(limit=5):
        """Fetches upcoming scheduled interviews for quick view."""
        interviews = Interview.query.filter_by(status="SCHEDULED").order_by(
            Interview.scheduled_at.asc()
        ).limit(limit).all()

        return [i.to_dict() for i in interviews]
