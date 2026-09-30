"""
Flask Extensions Module.

Instantiates extensions without binding them to any specific application instance.
The application factory pattern binds them inside create_app().
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
