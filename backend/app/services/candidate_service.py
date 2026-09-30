"""
Candidate Service.

Handles candidate CRUD, skill assignments, search, and filtering.
"""

from sqlalchemy import or_
from app.extensions import db
from app.models import Candidate, CandidateSkill, Skill
from app.utils.exceptions import ResourceNotFoundError, ValidationError, ConflictError


class CandidateService:
    @staticmethod
    def get_candidates(search=None, skill=None, location=None, min_exp=None, max_exp=None, status=None, page=1, per_page=50):
        """Retrieves candidates with multi-field filtering and pagination."""
        query = Candidate.query

        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Candidate.first_name.ilike(search_term),
                    Candidate.last_name.ilike(search_term),
                    Candidate.email.ilike(search_term),
                    Candidate.highest_qualification.ilike(search_term),
                    Candidate.current_company.ilike(search_term)
                )
            )

        if location:
            query = query.filter(Candidate.location.ilike(f"%{location.strip()}%"))

        if status:
            query = query.filter(Candidate.status == status.upper())

        if min_exp is not None:
            query = query.filter(Candidate.experience_years >= float(min_exp))

        if max_exp is not None:
            query = query.filter(Candidate.experience_years <= float(max_exp))

        if skill:
            query = query.join(Candidate.skills).join(CandidateSkill.skill).filter(
                Skill.name.ilike(f"%{skill.strip()}%")
            )

        query = query.order_by(Candidate.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [c.to_dict() for c in paginated.items],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages,
            "per_page": paginated.per_page
        }

    @staticmethod
    def get_candidate_by_id(candidate_id):
        """Retrieves candidate profile by ID."""
        candidate = db.session.get(Candidate, int(candidate_id))
        if not candidate:
            raise ResourceNotFoundError(f"Candidate with ID {candidate_id} not found")
        return candidate.to_dict()

    @staticmethod
    def create_candidate(data, created_by=None):
        """Creates a candidate record and assigns skills."""
        required = ["first_name", "last_name", "email", "phone", "location", "highest_qualification"]
        for field in required:
            if not data.get(field):
                raise ValidationError(f"Field '{field}' is required")

        email_clean = data["email"].strip().lower()
        if Candidate.query.filter_by(email=email_clean).first():
            raise ConflictError(f"Candidate with email '{email_clean}' already exists")

        candidate = Candidate(
            first_name=data["first_name"].strip(),
            last_name=data["last_name"].strip(),
            email=email_clean,
            phone=data["phone"].strip(),
            location=data["location"].strip(),
            experience_years=float(data.get("experience_years", 0.0)),
            highest_qualification=data["highest_qualification"].strip(),
            current_company=data.get("current_company"),
            current_ctc=data.get("current_ctc"),
            expected_ctc=data.get("expected_ctc"),
            resume_url=data.get("resume_url"),
            status=data.get("status", "AVAILABLE").upper(),
            created_by=created_by
        )
        db.session.add(candidate)
        db.session.flush()

        # Add skills
        skills_data = data.get("skills", [])
        CandidateService._assign_skills(candidate.id, skills_data)

        db.session.commit()
        return candidate.to_dict()

    @staticmethod
    def update_candidate(candidate_id, data):
        """Updates candidate details and skills."""
        candidate = db.session.get(Candidate, int(candidate_id))
        if not candidate:
            raise ResourceNotFoundError(f"Candidate with ID {candidate_id} not found")

        if "email" in data:
            email_clean = data["email"].strip().lower()
            existing = Candidate.query.filter_by(email=email_clean).first()
            if existing and existing.id != candidate.id:
                raise ConflictError(f"Email '{email_clean}' is already registered to another candidate")
            candidate.email = email_clean

        for field in ["first_name", "last_name", "phone", "location", "highest_qualification", "current_company", "resume_url"]:
            if field in data and data[field] is not None:
                setattr(candidate, field, str(data[field]).strip())

        if "experience_years" in data and data["experience_years"] is not None:
            candidate.experience_years = float(data["experience_years"])
        if "current_ctc" in data:
            candidate.current_ctc = data["current_ctc"]
        if "expected_ctc" in data:
            candidate.expected_ctc = data["expected_ctc"]
        if "status" in data and data["status"]:
            candidate.status = data["status"].upper()

        if "skills" in data:
            # Replace candidate skills
            CandidateSkill.query.filter_by(candidate_id=candidate.id).delete()
            CandidateService._assign_skills(candidate.id, data["skills"])

        db.session.commit()
        return candidate.to_dict()

    @staticmethod
    def delete_candidate(candidate_id):
        """Deletes a candidate record."""
        candidate = db.session.get(Candidate, int(candidate_id))
        if not candidate:
            raise ResourceNotFoundError(f"Candidate with ID {candidate_id} not found")
        db.session.delete(candidate)
        db.session.commit()
        return {"deleted": True, "id": candidate_id}

    @staticmethod
    def _assign_skills(candidate_id, skills_list):
        """Helper to create skill associations."""
        for item in skills_list:
            skill_name = item.get("skill_name") or item.get("name")
            if not skill_name:
                continue

            skill = Skill.query.filter(Skill.name.ilike(skill_name.strip())).first()
            if not skill:
                skill = Skill(name=skill_name.strip(), category=item.get("category", "General"))
                db.session.add(skill)
                db.session.flush()

            cand_skill = CandidateSkill(
                candidate_id=candidate_id,
                skill_id=skill.id,
                proficiency=item.get("proficiency", "INTERMEDIATE").upper()
            )
            db.session.add(cand_skill)

    @staticmethod
    def get_all_skills():
        """Returns all distinct skills available in catalog."""
        skills = Skill.query.order_by(Skill.name.asc()).all()
        return [s.to_dict() for s in skills]
