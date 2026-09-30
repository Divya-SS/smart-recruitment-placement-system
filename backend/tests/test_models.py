"""
Database Models Tests.

Verifies table creation, model attributes, and relational foreign keys.
"""

from app.models import (
    Role, User, Skill, Candidate, CandidateSkill,
    Company, Job, JobSkill, Application, Interview, InterviewFeedback
)


def test_user_password_hashing(db_session):
    """Verifies that bcrypt correctly hashes and verifies passwords."""
    role = Role(name="ADMIN", description="Administrator")
    db_session.add(role)
    db_session.commit()

    user = User(
        role_id=role.id,
        full_name="Admin User",
        email="admin@test.com"
    )
    user.set_password("Secret123!")
    db_session.add(user)
    db_session.commit()

    assert user.password_hash != "Secret123!"
    assert user.check_password("Secret123!") is True
    assert user.check_password("WrongPassword") is False


def test_candidate_skills_relationship(db_session):
    """Verifies Candidate and Skill many-to-many junction table."""
    python_skill = Skill(name="Python", category="Backend")
    flask_skill = Skill(name="Flask", category="Backend")
    db_session.add_all([python_skill, flask_skill])
    db_session.commit()

    candidate = Candidate(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="1234567890",
        location="New York",
        experience_years=3.5,
        highest_qualification="B.S. Computer Science"
    )
    db_session.add(candidate)
    db_session.commit()

    cand_skill1 = CandidateSkill(candidate_id=candidate.id, skill_id=python_skill.id, proficiency="EXPERT")
    cand_skill2 = CandidateSkill(candidate_id=candidate.id, skill_id=flask_skill.id, proficiency="INTERMEDIATE")
    db_session.add_all([cand_skill1, cand_skill2])
    db_session.commit()

    fetched = db_session.get(Candidate, candidate.id)
    assert len(fetched.skills) == 2
    assert fetched.full_name == "John Doe"
    assert {s.skill.name for s in fetched.skills} == {"Python", "Flask"}


def test_job_application_flow(db_session):
    """Verifies Job creation and Candidate application association."""
    company = Company(
        name="TechCorp Inc",
        location="San Francisco",
        contact_person_name="Jane Smith",
        contact_person_email="jane@techcorp.com",
        contact_person_phone="9876543210"
    )
    db_session.add(company)
    db_session.commit()

    job = Job(
        company_id=company.id,
        title="Full Stack Engineer",
        location="Remote",
        min_experience_years=2.0,
        job_type="FULL_TIME",
        openings_count=2
    )
    candidate = Candidate(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@test.com",
        phone="1234567890",
        location="Remote",
        experience_years=3.0,
        highest_qualification="B.Tech"
    )
    db_session.add_all([job, candidate])
    db_session.commit()

    application = Application(
        candidate_id=candidate.id,
        job_id=job.id,
        match_score=85.50,
        status="APPLIED"
    )
    db_session.add(application)
    db_session.commit()

    assert application.id is not None
    assert application.candidate.email == "jane.doe@test.com"
    assert application.job.title == "Full Stack Engineer"
