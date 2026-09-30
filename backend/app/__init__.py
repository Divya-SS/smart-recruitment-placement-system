"""
Application Factory Module.

Instantiates and configures the Flask application.
"""

import os
import logging
from flask import Flask
from config.config import get_config
from . import models
from app.extensions import db, migrate, jwt, cors
from app.utils.error_handlers import register_error_handlers
from app.routes import register_blueprints

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Flask Application Factory.

    :param config_name: 'development', 'testing', or 'production'
    :return: Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": config_obj.CORS_ORIGINS}})

    # Register blueprints & error handlers
    register_blueprints(app)
    register_error_handlers(app)

    # Register JWT error callbacks
    @jwt.unauthorized_loader
    def custom_unauthorized_response(err_str):
        return {
            "status": "error",
            "message": "Authorization token is missing or invalid",
            "data": None,
            "errors": err_str
        }, 401

    @jwt.expired_token_loader
    def custom_expired_token_response(jwt_header, jwt_payload):
        return {
            "status": "error",
            "message": "Token has expired. Please refresh your session.",
            "data": None,
            "errors": "token_expired"
        }, 401

    @jwt.invalid_token_loader
    def custom_invalid_token_response(err_str):
        return {
            "status": "error",
            "message": "Signature verification failed or token is malformed",
            "data": None,
            "errors": err_str
        }, 401

    logger.info(f"Flask App created with configuration: {config_obj.__name__}")
    return app
