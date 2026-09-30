"""
Candidate Matching Service.

Implements rule-based skill, experience, and location matching algorithm
between candidates and job openings.
"""

from app.extensions import db
from app.models import Job, Candidate, Application
from app.utils.exceptions import ResourceNotFoundError


class MatchingService:
    # Algorithm Weights
    WEIGHT_SKILLS = 0.65
    WEIGHT_EXPERIENCE = 0.25
    WEIGHT_LOCATION = 0.10

    @classmethod
    def calculate_match(cls, job, candidate):
        """
        Calculates detailed multi-factor match score between a Job and a Candidate.

        Returns:
            dict containing total_score, breakdown, matched_skills, missing_skills, and is_recommended.
        """
        # 1. Normalize Candidate Skills (case-insensitive set)
        cand_skill_map = {cs.skill.name.strip().lower(): cs.skill.name for cs in candidate.skills if cs.skill}
        cand_skill_keys = set(cand_skill_map.keys())

        # 2. Extract Job Skills
        job_mandatory = []
        job_optional = []
        for js in job.skills:
            if js.skill:
                if js.is_mandatory:
                    job_mandatory.append(js.skill.name.strip())
                else:
                    job_optional.append(js.skill.name.strip())

        all_job_skills = job_mandatory + job_optional
        all_job_keys = {s.lower(): s for s in all_job_skills}

        # Calculate Skill Compatibility
        matched_skills = []
        missing_skills = []

        for key, original_name in all_job_keys.items():
            if key in cand_skill_keys:
                matched_skills.append(original_name)
            else:
                missing_skills.append(original_name)

        if not all_job_skills:
            # If job specifies no skills, default to neutral score
            skill_score = 100.0
            mandatory_score = 100.0
            optional_score = 100.0
        else:
            mand_matched = [s for s in job_mandatory if s.lower() in cand_skill_keys]
            mand_count = len(job_mandatory)
            mandatory_score = (len(mand_matched) / mand_count * 100.0) if mand_count > 0 else 100.0

            opt_matched = [s for s in job_optional if s.lower() in cand_skill_keys]
            opt_count = len(job_optional)
            optional_score = (len(opt_matched) / opt_count * 100.0) if opt_count > 0 else 100.0

            if mand_count > 0 and opt_count > 0:
                skill_score = (0.80 * mandatory_score) + (0.20 * optional_score)
            elif mand_count > 0:
                skill_score = mandatory_score
            else:
                skill_score = optional_score

        # 3. Calculate Experience Score
        cand_exp = float(candidate.experience_years) if candidate.experience_years is not None else 0.0
        req_min_exp = float(job.min_experience_years) if job.min_experience_years is not None else 0.0

        if req_min_exp <= 0:
            exp_score = 100.0
        elif cand_exp >= req_min_exp:
            exp_score = 100.0
        else:
            exp_score = max(0.0, (cand_exp / req_min_exp) * 100.0)

        # 4. Calculate Location Score
        job_loc = (job.location or "").strip().lower()
        cand_loc = (candidate.location or "").strip().lower()

        if job_loc in ["remote", "any", "all", "wfh"] or job_loc == cand_loc:
            location_score = 100.0
        elif job_loc in cand_loc or cand_loc in job_loc:
            location_score = 75.0
        else:
            location_score = 0.0

        # 5. Total Composite Weighted Score
        total_score = (
            (cls.WEIGHT_SKILLS * skill_score) +
            (cls.WEIGHT_EXPERIENCE * exp_score) +
            (cls.WEIGHT_LOCATION * location_score)
        )
        total_score = round(min(100.0, max(0.0, total_score)), 2)

        return {
            "total_match_score": total_score,
            "skill_match_percentage": round(skill_score, 1),
            "experience_score": round(exp_score, 1),
            "location_score": round(location_score, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_required_skills": len(all_job_skills),
            "matched_count": len(matched_skills),
            "is_recommended": total_score >= 60.0
        }

    @classmethod
    def match_candidates_for_job(cls, job_id, min_score=0.0):
        """
        Evaluates and ranks all candidates against a specific job posting.
        """
        job = db.session.get(Job, int(job_id))
        if not job:
            raise ResourceNotFoundError(f"Job with ID {job_id} not found")

        candidates = Candidate.query.filter(Candidate.status != "INACTIVE").all()
        results = []

        # Find existing applications for this job to flag applied status
        existing_apps = {
            app.candidate_id: app.status 
            for app in Application.query.filter_by(job_id=job.id).all()
        }

        for candidate in candidates:
            match_data = cls.calculate_match(job, candidate)
            if match_data["total_match_score"] >= float(min_score):
                cand_dict = candidate.to_dict()
                cand_dict["application_status"] = existing_apps.get(candidate.id, None)
                results.append({
                    "candidate": cand_dict,
                    "match": match_data
                })

        # Sort descending by match score
        results.sort(key=lambda x: x["match"]["total_match_score"], reverse=True)

        return {
            "job": job.to_dict(),
            "candidates_evaluated": len(candidates),
            "matches": results
        }

    @classmethod
    def match_jobs_for_candidate(cls, candidate_id, min_score=0.0):
        """
        Evaluates and ranks open jobs for a specific candidate.
        """
        candidate = db.session.get(Candidate, int(candidate_id))
        if not candidate:
            raise ResourceNotFoundError(f"Candidate with ID {candidate_id} not found")

        open_jobs = Job.query.filter(Job.status == "OPEN").all()
        results = []

        existing_apps = {
            app.job_id: app.status
            for app in Application.query.filter_by(candidate_id=candidate.id).all()
        }

        for job in open_jobs:
            match_data = cls.calculate_match(job, candidate)
            if match_data["total_match_score"] >= float(min_score):
                job_dict = job.to_dict()
                job_dict["application_status"] = existing_apps.get(job.id, None)
                results.append({
                    "job": job_dict,
                    "match": match_data
                })

        results.sort(key=lambda x: x["match"]["total_match_score"], reverse=True)

        return {
            "candidate": candidate.to_dict(),
            "jobs_evaluated": len(open_jobs),
            "matches": results
        }
