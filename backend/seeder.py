"""
Database Seeder Script.

Populates the MySQL database with realistic initial roles, users, companies,
jobs, candidates with skill associations, applications, and interview data.
"""

from datetime import datetime, timezone, timedelta
from app import create_app
from app.extensions import db
from app.models import (
    Role, User, Skill, Company, Job, JobSkill,
    Candidate, CandidateSkill, Application, Interview, InterviewFeedback
)
from app.services.matching_service import MatchingService


def seed_database():
    app = create_app()
    with app.app_context():
        print("[*] Starting Database Seeding Process...")

        # 1. Seed Roles
        admin_role = Role.query.filter_by(name="ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN", description="Full system access and user management")
            db.session.add(admin_role)

        recruiter_role = Role.query.filter_by(name="RECRUITER").first()
        if not recruiter_role:
            recruiter_role = Role(name="RECRUITER", description="Candidate pipeline and interview management")
            db.session.add(recruiter_role)

        db.session.commit()
        print("[+] Roles seeded.")

        # 2. Seed Users
        admin_user = User.query.filter_by(email="admin@recruitment.com").first()
        if not admin_user:
            admin_user = User(
                role_id=admin_role.id,
                full_name="Sarah Connor (Lead Admin)",
                email="admin@recruitment.com",
                phone="+1 (555) 019-2831",
                is_active=True
            )
            admin_user.set_password("Admin@123")
            db.session.add(admin_user)

        recruiter_user = User.query.filter_by(email="recruiter@recruitment.com").first()
        if not recruiter_user:
            recruiter_user = User(
                role_id=recruiter_role.id,
                full_name="Alex Morgan (Senior Recruiter)",
                email="recruiter@recruitment.com",
                phone="+1 (555) 018-9922",
                is_active=True
            )
            recruiter_user.set_password("Recruiter@123")
            db.session.add(recruiter_user)

        db.session.commit()
        print("[+] Users seeded (admin@recruitment.com / Admin@123, recruiter@recruitment.com / Recruiter@123).")

        # 3. Seed Skills
        skills_catalog = [
            ("Python", "Backend"),
            ("Flask", "Backend"),
            ("Django", "Backend"),
            ("FastAPI", "Backend"),
            ("Java", "Backend"),
            ("Spring Boot", "Backend"),
            ("Node.js", "Backend"),
            ("JavaScript", "Frontend"),
            ("TypeScript", "Frontend"),
            ("React.js", "Frontend"),
            ("Vue.js", "Frontend"),
            ("HTML5", "Frontend"),
            ("CSS3", "Frontend"),
            ("TailwindCSS", "Frontend"),
            ("MySQL", "Database"),
            ("PostgreSQL", "Database"),
            ("MongoDB", "Database"),
            ("Redis", "Database"),
            ("Git", "DevOps"),
            ("Docker", "DevOps"),
            ("Kubernetes", "DevOps"),
            ("AWS", "Cloud"),
            ("Azure", "Cloud"),
            ("REST APIs", "Architecture"),
            ("GraphQL", "Architecture")
        ]

        skill_objs = {}
        for name, category in skills_catalog:
            skill = Skill.query.filter_by(name=name).first()
            if not skill:
                skill = Skill(name=name, category=category)
                db.session.add(skill)
                db.session.flush()
            skill_objs[name] = skill

        db.session.commit()
        print("[+] Skills catalog seeded.")

        # 4. Seed Companies
        companies_data = [
            {
                "name": "Acme Innovations Ltd",
                "website": "https://acme-innovations.io",
                "industry": "FinTech / SaaS",
                "location": "San Francisco, CA",
                "contact_person_name": "Elena Rostova",
                "contact_person_email": "elena.r@acme-innovations.io",
                "contact_person_phone": "+1 415 555 0101",
                "status": "ACTIVE"
            },
            {
                "name": "CloudScale Systems",
                "website": "https://cloudscale.tech",
                "industry": "Cloud Infrastructure",
                "location": "Seattle, WA",
                "contact_person_name": "Marcus Vance",
                "contact_person_email": "marcus.v@cloudscale.tech",
                "contact_person_phone": "+1 206 555 0142",
                "status": "ACTIVE"
            },
            {
                "name": "Nexus AI Robotics",
                "website": "https://nexus-ai.dev",
                "industry": "Artificial Intelligence",
                "location": "Boston, MA",
                "contact_person_name": "Dr. Aris Thorne",
                "contact_person_email": "aris@nexus-ai.dev",
                "contact_person_phone": "+1 617 555 0188",
                "status": "ACTIVE"
            },
            {
                "name": "Apex Global Solutions",
                "website": "https://apexsolutions.com",
                "industry": "Enterprise Consulting",
                "location": "New York, NY",
                "contact_person_name": "Chloe Bennett",
                "contact_person_email": "c.bennett@apexsolutions.com",
                "contact_person_phone": "+1 212 555 0199",
                "status": "ACTIVE"
            }
        ]

        company_objs = []
        for cdata in companies_data:
            c = Company.query.filter_by(name=cdata["name"]).first()
            if not c:
                c = Company(**cdata)
                db.session.add(c)
                db.session.flush()
            company_objs.append(c)

        db.session.commit()
        print("[+] Companies seeded.")

        # 5. Seed Jobs
        jobs_data = [
            {
                "company_id": company_objs[0].id,
                "title": "Senior Python / Flask Backend Engineer",
                "description": "Lead the design and development of high-throughput REST APIs and microservices for financial transaction processing.",
                "min_experience_years": 3.0,
                "max_experience_years": 6.0,
                "qualification_required": "B.S. in Computer Science or equivalent",
                "location": "San Francisco, CA",
                "job_type": "FULL_TIME",
                "min_salary": 120000,
                "max_salary": 160000,
                "openings_count": 3,
                "status": "OPEN",
                "assigned_recruiter_id": recruiter_user.id,
                "skills": [
                    ("Python", True),
                    ("Flask", True),
                    ("MySQL", True),
                    ("REST APIs", True),
                    ("Docker", False),
                    ("Redis", False)
                ]
            },
            {
                "company_id": company_objs[1].id,
                "title": "Full Stack React & Node Developer",
                "description": "Build interactive customer dashboards and cloud resource provisioning consoles using modern React and TypeScript.",
                "min_experience_years": 2.0,
                "max_experience_years": 5.0,
                "qualification_required": "Bachelor's Degree in Software Engineering",
                "location": "Seattle, WA",
                "job_type": "FULL_TIME",
                "min_salary": 105000,
                "max_salary": 140000,
                "openings_count": 2,
                "status": "OPEN",
                "assigned_recruiter_id": recruiter_user.id,
                "skills": [
                    ("React.js", True),
                    ("JavaScript", True),
                    ("TypeScript", True),
                    ("Node.js", True),
                    ("TailwindCSS", False),
                    ("Git", True)
                ]
            },
            {
                "company_id": company_objs[2].id,
                "title": "Junior Python Developer (Placement Track)",
                "description": "Exciting entry-level role for talented junior developers to learn FastAPI, data ingestion pipelines, and REST architectures.",
                "min_experience_years": 0.5,
                "max_experience_years": 2.0,
                "qualification_required": "B.Tech / B.E. / BCA / MCA",
                "location": "Boston, MA",
                "job_type": "FULL_TIME",
                "min_salary": 70000,
                "max_salary": 90000,
                "openings_count": 5,
                "status": "OPEN",
                "assigned_recruiter_id": recruiter_user.id,
                "skills": [
                    ("Python", True),
                    ("MySQL", True),
                    ("Git", True),
                    ("REST APIs", False)
                ]
            },
            {
                "company_id": company_objs[3].id,
                "title": "DevOps & Cloud Automation Engineer",
                "description": "Maintain CI/CD pipelines, Kubernetes orchestration clusters, and infrastructure as code across AWS environments.",
                "min_experience_years": 3.5,
                "max_experience_years": 7.0,
                "qualification_required": "B.S. in IT or relevant engineering discipline",
                "location": "Remote",
                "job_type": "FULL_TIME",
                "min_salary": 130000,
                "max_salary": 175000,
                "openings_count": 1,
                "status": "OPEN",
                "assigned_recruiter_id": admin_user.id,
                "skills": [
                    ("Docker", True),
                    ("Kubernetes", True),
                    ("AWS", True),
                    ("Git", True),
                    ("Python", False)
                ]
            }
        ]

        job_objs = []
        for jdata in jobs_data:
            skills_req = jdata.pop("skills")
            j = Job.query.filter_by(title=jdata["title"], company_id=jdata["company_id"]).first()
            if not j:
                j = Job(**jdata, created_by=admin_user.id)
                db.session.add(j)
                db.session.flush()

                for s_name, mandatory in skills_req:
                    if s_name in skill_objs:
                        js = JobSkill(job_id=j.id, skill_id=skill_objs[s_name].id, is_mandatory=mandatory)
                        db.session.add(js)

            job_objs.append(j)

        db.session.commit()
        print("[+] Jobs & required skills seeded.")

        # 6. Seed Candidates
        candidates_data = [
            {
                "first_name": "Daniel",
                "last_name": "Ribeiro",
                "email": "daniel.ribeiro@example.com",
                "phone": "+1 415 555 8312",
                "location": "San Francisco, CA",
                "experience_years": 4.0,
                "highest_qualification": "B.S. Computer Science",
                "current_company": "ByteCraft Labs",
                "current_ctc": 110000,
                "expected_ctc": 135000,
                "status": "AVAILABLE",
                "skills": [("Python", "EXPERT"), ("Flask", "EXPERT"), ("MySQL", "EXPERT"), ("REST APIs", "EXPERT"), ("Docker", "INTERMEDIATE"), ("Git", "EXPERT")]
            },
            {
                "first_name": "Sophia",
                "last_name": "Chen",
                "email": "sophia.chen@example.com",
                "phone": "+1 206 555 4910",
                "location": "Seattle, WA",
                "experience_years": 3.0,
                "highest_qualification": "B.E. Information Technology",
                "current_company": "Northwest Pixel",
                "current_ctc": 95000,
                "expected_ctc": 120000,
                "status": "AVAILABLE",
                "skills": [("React.js", "EXPERT"), ("JavaScript", "EXPERT"), ("TypeScript", "INTERMEDIATE"), ("Node.js", "INTERMEDIATE"), ("TailwindCSS", "EXPERT"), ("Git", "EXPERT")]
            },
            {
                "first_name": "Rohan",
                "last_name": "Sharma",
                "email": "rohan.sharma@example.com",
                "phone": "+1 617 555 7721",
                "location": "Boston, MA",
                "experience_years": 1.0,
                "highest_qualification": "B.Tech Computer Science",
                "current_company": "Apex Graduate Intern",
                "current_ctc": 60000,
                "expected_ctc": 80000,
                "status": "AVAILABLE",
                "skills": [("Python", "INTERMEDIATE"), ("MySQL", "INTERMEDIATE"), ("Git", "INTERMEDIATE"), ("Flask", "BEGINNER"), ("REST APIs", "INTERMEDIATE")]
            },
            {
                "first_name": "Emily",
                "last_name": "Watson",
                "email": "emily.watson@example.com",
                "phone": "+1 512 555 3309",
                "location": "Remote",
                "experience_years": 5.0,
                "highest_qualification": "M.S. Cloud Computing",
                "current_company": "CloudForge Tech",
                "current_ctc": 135000,
                "expected_ctc": 160000,
                "status": "AVAILABLE",
                "skills": [("Docker", "EXPERT"), ("Kubernetes", "EXPERT"), ("AWS", "EXPERT"), ("Git", "EXPERT"), ("Python", "INTERMEDIATE")]
            },
            {
                "first_name": "Lucas",
                "last_name": "Vargas",
                "email": "lucas.vargas@example.com",
                "phone": "+1 312 555 9012",
                "location": "Chicago, IL",
                "experience_years": 2.5,
                "highest_qualification": "B.S. Software Engineering",
                "current_company": "Midwest Data",
                "current_ctc": 85000,
                "expected_ctc": 105000,
                "status": "AVAILABLE",
                "skills": [("Python", "INTERMEDIATE"), ("Django", "INTERMEDIATE"), ("PostgreSQL", "INTERMEDIATE"), ("REST APIs", "INTERMEDIATE"), ("Git", "INTERMEDIATE")]
            }
        ]

        cand_objs = []
        for cdata in candidates_data:
            cskills = cdata.pop("skills")
            c = Candidate.query.filter_by(email=cdata["email"]).first()
            if not c:
                c = Candidate(**cdata, created_by=recruiter_user.id)
                db.session.add(c)
                db.session.flush()

                for s_name, prof in cskills:
                    if s_name in skill_objs:
                        cs = CandidateSkill(candidate_id=c.id, skill_id=skill_objs[s_name].id, proficiency=prof)
                        db.session.add(cs)

            cand_objs.append(c)

        db.session.commit()
        print("[+] Candidates & skill proficiencies seeded.")

        # 7. Seed Applications
        app_mappings = [
            (cand_objs[0], job_objs[0], "SHORTLISTED", "Candidate has outstanding Flask and MySQL mastery."),
            (cand_objs[1], job_objs[1], "INTERVIEW_SCHEDULED", "Strong portfolio with TypeScript & React component libraries."),
            (cand_objs[2], job_objs[2], "APPLIED", "Promising graduate candidate matching our Junior track."),
            (cand_objs[3], job_objs[3], "SELECTED", "Exceptional Kubernetes architectural experience."),
        ]

        app_objs = []
        for cand, job, status, notes in app_mappings:
            app_rec = Application.query.filter_by(candidate_id=cand.id, job_id=job.id).first()
            if not app_rec:
                match_res = MatchingService.calculate_match(job, cand)
                app_rec = Application(
                    candidate_id=cand.id,
                    job_id=job.id,
                    match_score=match_res["total_match_score"],
                    status=status,
                    notes=notes
                )
                db.session.add(app_rec)
                db.session.flush()
            app_objs.append(app_rec)

        db.session.commit()
        print("[+] Job Applications seeded.")

        # 8. Seed Interviews & Feedback
        interview_time = datetime.now(timezone.utc) + timedelta(days=2, hours=3)
        interview_past = datetime.now(timezone.utc) - timedelta(days=1, hours=2)

        # Scheduled upcoming interview
        inv1 = Interview.query.filter_by(application_id=app_objs[1].id).first()
        if not inv1:
            inv1 = Interview(
                application_id=app_objs[1].id,
                scheduled_by=recruiter_user.id,
                interview_round="Technical Round 1 (Frontend Architecture)",
                scheduled_at=interview_time,
                mode="ONLINE",
                meeting_link_or_venue="https://meet.google.com/xyz-recruitment-demo",
                interviewer_name="Dr. Kevin Nolan (Lead Architect)",
                interviewer_email="kevin.n@cloudscale.tech",
                status="SCHEDULED"
            )
            db.session.add(inv1)

        # Completed past interview with Feedback
        inv2 = Interview.query.filter_by(application_id=app_objs[3].id).first()
        if not inv2:
            inv2 = Interview(
                application_id=app_objs[3].id,
                scheduled_by=admin_user.id,
                interview_round="Final Technical Deep-Dive",
                scheduled_at=interview_past,
                mode="ONLINE",
                meeting_link_or_venue="https://meet.google.com/apex-final-round",
                interviewer_name="Chloe Bennett (VP Engineering)",
                interviewer_email="c.bennett@apexsolutions.com",
                status="COMPLETED"
            )
            db.session.add(inv2)
            db.session.flush()

            feedback = InterviewFeedback(
                interview_id=inv2.id,
                technical_rating=5,
                communication_rating=5,
                overall_rating=5,
                comments="Exceptional mastery of AWS infrastructure, Dockerized workloads, and CI/CD pipelines. Strong Hire!",
                recommendation="STRONG_HIRE"
            )
            db.session.add(feedback)

        db.session.commit()
        print("[+] Interviews and evaluation feedback seeded.")
        print("\n[+] Database Seeding Complete! Ready to launch.")


if __name__ == "__main__":
    seed_database()
