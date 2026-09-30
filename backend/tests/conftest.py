"""
Pytest Test Fixtures Configuration.

Creates an isolated testing application instance with an in-memory SQLite database.
"""

import pytest
from app import create_app
from app.extensions import db


@pytest.fixture(scope="session")
def app():
    """Create and configure a testing Flask application."""
    test_app = create_app("testing")
    
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Provides a test client for invoking API routes."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Provides a CLI test runner."""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def db_session(app):
    """Provides a clean database session wrapped in a transaction rollback."""
    with app.app_context():
        # Clear tables between tests
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        yield db.session
        db.session.rollback()
