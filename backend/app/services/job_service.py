"""
Job Service.

Handles job posting lifecycle, requirement management, and skill mappings.
"""

from datetime import datetime
from sqlalchemy import or_
from app.extensions import db
from app.models import Job, JobSkill, Skill, Company
from app.utils.exceptions import ResourceNotFoundError, ValidationError


class JobService:
    @staticmethod
    def get_jobs(search=None, company_id=None, recruiter_id=None, status=None, job_type=None, location=None, page=1, per_page=50):
        """Fetches jobs with filters and pagination."""
        query = Job.query

        if search:
            search_term = f"%{search.strip()}%"
            query = query.join(Company).filter(
                or_(
                    Job.title.ilike(search_term),
                    Job.location.ilike(search_term),
                    Job.qualification_required.ilike(search_term),
                    Company.name.ilike(search_term)
                )
            )

        if company_id:
            query = query.filter(Job.company_id == int(company_id))

        if recruiter_id:
            query = query.filter(Job.assigned_recruiter_id == int(recruiter_id))

        if status:
            query = query.filter(Job.status == status.upper())

        if job_type:
            query = query.filter(Job.job_type == job_type.upper())

        if location:
            query = query.filter(Job.location.ilike(f"%{location.strip()}%"))

        query = query.order_by(Job.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [j.to_dict() for j in paginated.items],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages,
            "per_page": paginated.per_page
        }

    @staticmethod
    def get_job_by_id(job_id):
        """Retrieves job by ID."""
        job = db.session.get(Job, int(job_id))
        if not job:
            raise ResourceNotFoundError(f"Job with ID {job_id} not found")
        data = job.to_dict()
        data["applications_count"] = len(job.applications)
        return data

    @staticmethod
    def create_job(data, created_by=None):
        """Creates a new job posting with skill requirements."""
        required = ["company_id", "title", "location"]
        for field in required:
            if not data.get(field):
                raise ValidationError(f"Field '{field}' is required")

        company = db.session.get(Company, int(data["company_id"]))
        if not company:
            raise ValidationError(f"Company ID {data['company_id']} does not exist")

        deadline_val = None
        if data.get("deadline"):
            try:
                deadline_val = datetime.strptime(data["deadline"], "%Y-%m-%d").date()
            except Exception:
                pass

        job = Job(
            company_id=int(data["company_id"]),
            created_by=created_by,
            assigned_recruiter_id=data.get("assigned_recruiter_id"),
            title=data["title"].strip(),
            description=data.get("description"),
            min_experience_years=float(data.get("min_experience_years", 0.0)),
            max_experience_years=float(data["max_experience_years"]) if data.get("max_experience_years") else None,
            qualification_required=data.get("qualification_required"),
            location=data["location"].strip(),
            job_type=data.get("job_type", "FULL_TIME").upper(),
            min_salary=data.get("min_salary"),
            max_salary=data.get("max_salary"),
            openings_count=int(data.get("openings_count", 1)),
            status=data.get("status", "OPEN").upper(),
            deadline=deadline_val
        )
        db.session.add(job)
        db.session.flush()

        # Add skills
        skills_data = data.get("skills", [])
        JobService._assign_skills(job.id, skills_data)

        db.session.commit()
        return job.to_dict()

    @staticmethod
    def update_job(job_id, data):
        """Updates job information and skills."""
        job = db.session.get(Job, int(job_id))
        if not job:
            raise ResourceNotFoundError(f"Job with ID {job_id} not found")

        for field in ["title", "description", "location", "qualification_required"]:
            if field in data and data[field] is not None:
                setattr(job, field, str(data[field]).strip())

        if "company_id" in data and data["company_id"]:
            job.company_id = int(data["company_id"])
        if "assigned_recruiter_id" in data:
            job.assigned_recruiter_id = data["assigned_recruiter_id"]
        if "min_experience_years" in data and data["min_experience_years"] is not None:
            job.min_experience_years = float(data["min_experience_years"])
        if "max_experience_years" in data:
            job.max_experience_years = float(data["max_experience_years"]) if data["max_experience_years"] else None
        if "job_type" in data and data["job_type"]:
            job.job_type = data["job_type"].upper()
        if "min_salary" in data:
            job.min_salary = data["min_salary"]
        if "max_salary" in data:
            job.max_salary = data["max_salary"]
        if "openings_count" in data and data["openings_count"] is not None:
            job.openings_count = int(data["openings_count"])
        if "status" in data and data["status"]:
            job.status = data["status"].upper()

        if "deadline" in data:
            if data["deadline"]:
                try:
                    job.deadline = datetime.strptime(data["deadline"], "%Y-%m-%d").date()
                except Exception:
                    pass
            else:
                job.deadline = None

        if "skills" in data:
            JobSkill.query.filter_by(job_id=job.id).delete()
            JobService._assign_skills(job.id, data["skills"])

        db.session.commit()
        return job.to_dict()

    @staticmethod
    def delete_job(job_id):
        """Deletes a job posting."""
        job = db.session.get(Job, int(job_id))
        if not job:
            raise ResourceNotFoundError(f"Job with ID {job_id} not found")
        db.session.delete(job)
        db.session.commit()
        return {"deleted": True, "id": job_id}

    @staticmethod
    def _assign_skills(job_id, skills_list):
        """Helper to create job skill associations."""
        for item in skills_list:
            skill_name = item.get("skill_name") or item.get("name")
            if not skill_name:
                continue

            skill = Skill.query.filter(Skill.name.ilike(skill_name.strip())).first()
            if not skill:
                skill = Skill(name=skill_name.strip(), category=item.get("category", "General"))
                db.session.add(skill)
                db.session.flush()

            job_skill = JobSkill(
                job_id=job_id,
                skill_id=skill.id,
                is_mandatory=item.get("is_mandatory", True)
            )
            db.session.add(job_skill)
