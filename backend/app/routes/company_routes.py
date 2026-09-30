"""
Company Routes.

CRUD and search endpoints for partner companies.
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.company_service import CompanyService
from app.utils.response import success_response
from app.utils.decorators import admin_required

company_bp = Blueprint("companies", __name__, url_prefix="/api/companies")


@company_bp.route("", methods=["GET"])
@jwt_required()
def list_companies():
    """List companies with search and filters."""
    search = request.args.get("search")
    status = request.args.get("status")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))

    result = CompanyService.get_companies(search=search, status=status, page=page, per_page=per_page)
    return success_response(data=result)


@company_bp.route("/<int:company_id>", methods=["GET"])
@jwt_required()
def get_company(company_id):
    """Get single company details."""
    company = CompanyService.get_company_by_id(company_id)
    return success_response(data=company)


@company_bp.route("", methods=["POST"])
@admin_required()
def create_company():
    """Create new company (Admin only)."""
    data = request.get_json() or {}
    company = CompanyService.create_company(data)
    return success_response(message="Company created successfully", data=company, status_code=201)


@company_bp.route("/<int:company_id>", methods=["PUT"])
@admin_required()
def update_company(company_id):
    """Update company details (Admin only)."""
    data = request.get_json() or {}
    company = CompanyService.update_company(company_id, data)
    return success_response(message="Company updated successfully", data=company)


@company_bp.route("/<int:company_id>", methods=["DELETE"])
@admin_required()
def delete_company(company_id):
    """Delete company (Admin only)."""
    result = CompanyService.delete_company(company_id)
    return success_response(message="Company deleted successfully", data=result)
