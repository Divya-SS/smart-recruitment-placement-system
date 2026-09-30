"""
Comprehensive API Integration Tests.

Tests Auth, Candidates, Jobs, Rule-Based Matching Engine, and Applications.
"""

import json
from app.models import Role, User, Candidate, Job, Company, Skill, CandidateSkill, JobSkill


def test_auth_login_success(client, db_session):
    role = Role(name="ADMIN", description="Admin")
    db_session.add(role)
    db_session.flush()

    user = User(role_id=role.id, full_name="Admin Test", email="admin_test@test.com")
    user.set_password("Admin@123")
    db_session.add(user)
    db_session.commit()

    resp = client.post("/api/auth/login", json={"email": "admin_test@test.com", "password": "Admin@123"})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert data["data"]["user"]["email"] == "admin_test@test.com"


def test_matching_engine_accuracy(client, db_session):
    """Verifies that rule-based matching calculates accurate scores and breakdown."""
    # Setup skills
    py = Skill(name="Python", category="Backend")
    fl = Skill(name="Flask", category="Backend")
    sq = Skill(name="MySQL", category="Database")
    db_session.add_all([py, fl, sq])
    db_session.flush()

    comp = Company(name="TestCorp", location="SF", contact_person_name="HR", contact_person_email="hr@test.com", contact_person_phone="123")
    db_session.add(comp)
    db_session.flush()

    job = Job(
        company_id=comp.id,
        title="Python Dev",
        location="SF",
        min_experience_years=2.0,
        job_type="FULL_TIME"
    )
    db_session.add(job)
    db_session.flush()

    # Job requires Python and Flask
    js1 = JobSkill(job_id=job.id, skill_id=py.id, is_mandatory=True)
    js2 = JobSkill(job_id=job.id, skill_id=fl.id, is_mandatory=True)
    db_session.add_all([js1, js2])

    # Candidate 1 has Python, Flask, MySQL, 3 years exp, SF location -> should match 100%
    cand1 = Candidate(
        first_name="Alice", last_name="Dev", email="alice@test.com", phone="123",
        location="SF", experience_years=3.0, highest_qualification="B.Tech"
    )
    db_session.add(cand1)
    db_session.flush()

    cs1 = CandidateSkill(candidate_id=cand1.id, skill_id=py.id, proficiency="EXPERT")
    cs2 = CandidateSkill(candidate_id=cand1.id, skill_id=fl.id, proficiency="EXPERT")
    cs3 = CandidateSkill(candidate_id=cand1.id, skill_id=sq.id, proficiency="EXPERT")
    db_session.add_all([cs1, cs2, cs3])
    db_session.commit()

    # Login to get JWT
    role = Role(name="ADMIN")
    db_session.add(role)
    db_session.flush()
    u = User(role_id=role.id, full_name="Tester", email="t@test.com")
    u.set_password("pass")
    db_session.add(u)
    db_session.commit()

    login_resp = client.post("/api/auth/login", json={"email": "t@test.com", "password": "pass"})
    token = json.loads(login_resp.data)["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test matching endpoint
    resp = client.get(f"/api/matching/job/{job.id}", headers=headers)
    assert resp.status_code == 200
    res_data = json.loads(resp.data)["data"]
    assert res_data["candidates_evaluated"] >= 1
    top_match = res_data["matches"][0]
    assert top_match["candidate"]["email"] == "alice@test.com"
    assert top_match["match"]["skill_match_percentage"] == 100.0
    assert top_match["match"]["total_match_score"] == 100.0
    assert "Python" in top_match["match"]["matched_skills"]
    assert "Flask" in top_match["match"]["matched_skills"]
