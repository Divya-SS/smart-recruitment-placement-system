"""
Routes Package.

Registers all modular API blueprints.
"""

from .health_routes import health_bp
from .auth_routes import auth_bp
from .candidate_routes import candidate_bp
from .company_routes import company_bp
from .job_routes import job_bp
from .matching_routes import matching_bp
from .application_routes import application_bp
from .interview_routes import interview_bp
from .dashboard_routes import dashboard_bp
from .user_routes import user_bp


def register_blueprints(app):
    """Registers all API blueprints to the Flask app instance."""
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(user_bp)
