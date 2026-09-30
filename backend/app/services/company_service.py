"""
Company Service.

Handles client company registration, listing, and updates.
"""

from sqlalchemy import or_
from app.extensions import db
from app.models import Company
from app.utils.exceptions import ResourceNotFoundError, ValidationError, ConflictError


class CompanyService:
    @staticmethod
    def get_companies(search=None, status=None, page=1, per_page=50):
        """Fetches companies with search and pagination."""
        query = Company.query

        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Company.name.ilike(search_term),
                    Company.location.ilike(search_term),
                    Company.industry.ilike(search_term),
                    Company.contact_person_name.ilike(search_term),
                    Company.contact_person_email.ilike(search_term)
                )
            )

        if status:
            query = query.filter(Company.status == status.upper())

        query = query.order_by(Company.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [c.to_dict() for c in paginated.items],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages,
            "per_page": paginated.per_page
        }

    @staticmethod
    def get_company_by_id(company_id):
        """Retrieves company by ID."""
        company = db.session.get(Company, int(company_id))
        if not company:
            raise ResourceNotFoundError(f"Company with ID {company_id} not found")
        data = company.to_dict()
        data["jobs_count"] = len(company.jobs)
        return data

    @staticmethod
    def create_company(data):
        """Creates a new company record."""
        required = ["name", "location", "contact_person_name", "contact_person_email", "contact_person_phone"]
        for field in required:
            if not data.get(field):
                raise ValidationError(f"Field '{field}' is required")

        name_clean = data["name"].strip()
        if Company.query.filter_by(name=name_clean).first():
            raise ConflictError(f"Company '{name_clean}' already exists")

        company = Company(
            name=name_clean,
            website=data.get("website"),
            industry=data.get("industry"),
            location=data["location"].strip(),
            contact_person_name=data["contact_person_name"].strip(),
            contact_person_email=data["contact_person_email"].strip(),
            contact_person_phone=data["contact_person_phone"].strip(),
            status=data.get("status", "ACTIVE").upper()
        )
        db.session.add(company)
        db.session.commit()
        return company.to_dict()

    @staticmethod
    def update_company(company_id, data):
        """Updates company details."""
        company = db.session.get(Company, int(company_id))
        if not company:
            raise ResourceNotFoundError(f"Company with ID {company_id} not found")

        if "name" in data:
            name_clean = data["name"].strip()
            existing = Company.query.filter_by(name=name_clean).first()
            if existing and existing.id != company.id:
                raise ConflictError(f"Company name '{name_clean}' already in use")
            company.name = name_clean

        for field in ["website", "industry", "location", "contact_person_name", "contact_person_email", "contact_person_phone"]:
            if field in data and data[field] is not None:
                setattr(company, field, str(data[field]).strip())

        if "status" in data and data["status"]:
            company.status = data["status"].upper()

        db.session.commit()
        return company.to_dict()

    @staticmethod
    def delete_company(company_id):
        """Deletes a company record."""
        company = db.session.get(Company, int(company_id))
        if not company:
            raise ResourceNotFoundError(f"Company with ID {company_id} not found")
        db.session.delete(company)
        db.session.commit()
        return {"deleted": True, "id": company_id}
