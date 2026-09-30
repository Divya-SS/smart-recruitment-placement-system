# Database Design & Schema Specification
## Smart Recruitment & Placement Management System (SRPMS)

### 1. Normalized Relational Schema (3NF)

#### Entities
1. **`roles`**: System permissions (`ADMIN`, `RECRUITER`).
2. **`users`**: Admins and Recruiters with hashed credentials (`bcrypt`).
3. **`skills`**: Standardized skills catalog.
4. **`candidates`**: Candidate profiles, contact details, experience, qualification.
5. **`candidate_skills`**: Many-to-many junction between candidates and skills with proficiency levels.
6. **`companies`**: Client companies offering hiring opportunities.
7. **`jobs`**: Job postings with openings, salary, and requirements.
8. **`job_skills`**: Many-to-many junction between jobs and required skills (mandatory/optional).
9. **`applications`**: Mapping candidates to jobs with status (`APPLIED`, `SHORTLISTED`, `INTERVIEW_SCHEDULED`, `SELECTED`, `REJECTED`, `JOINED`).
10. **`interviews`**: Scheduled interview rounds, dates, modes, and interviewer info.
11. **`interview_feedback`**: Ratings (1-5), comments, and hiring recommendations.

### 2. Indexes & Performance Optimization
- B-Tree indexes placed on primary lookup columns: `email`, `location`, `status`, `name`, `scheduled_at`.
- Foreign key constraints with `ON DELETE CASCADE` on child junction tables and `ON DELETE RESTRICT` / `SET NULL` on historical records.
