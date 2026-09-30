"""
Skill Model Module.

Catalog of normalized skills.
"""

from app.extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=True, index=True)

    # Relationships
    candidate_associations = db.relationship(
        "CandidateSkill", back_populates="skill", cascade="all, delete-orphan", lazy="select"
    )
    job_associations = db.relationship(
        "JobSkill", back_populates="skill", cascade="all, delete-orphan", lazy="select"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }

    def __repr__(self):
        return f"<Skill id={self.id} name='{self.name}'>"
