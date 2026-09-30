"""
Base Model Module.

Provides standard ID and Timestamp mixins for all database entities.
"""

from datetime import datetime, timezone
from app.extensions import db


class TimestampMixin:
    """Provides auto-managed created_at and updated_at datetime columns."""
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class BaseModel(db.Model, TimestampMixin):
    """Abstract base model with primary key and timestamps."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        """Converts model column values to a dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
