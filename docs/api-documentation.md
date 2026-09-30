# REST API Specification
## Smart Recruitment & Placement Management System (SRPMS)

### Base URL
`http://localhost:5000/api`

---

### Endpoints Overview

#### 1. System Health & Liveness
- `GET /api/health`
  - Response (200 OK):
    ```json
    {
      "status": "success",
      "message": "Smart Recruitment API is running"
    }
    ```
- `GET /api/health/db`
  - Response (200 OK):
    ```json
    {
      "status": "success",
      "message": "Database connection is healthy",
      "database": "connected"
    }
    ```

---

#### 2. Planned Modules (Subsequent Phases)
- **Auth:** `/api/auth/login`, `/api/auth/refresh`, `/api/auth/me`
- **Candidates:** `/api/candidates` (CRUD, Search & Filter)
- **Companies:** `/api/companies` (CRUD)
- **Jobs:** `/api/jobs` (CRUD, Skills Mapping)
- **Matching Engine:** `/api/matching/job/<id>`, `/api/matching/candidate/<id>`
- **Applications:** `/api/applications` (Lifecycle Progression)
- **Interviews:** `/api/interviews` (Scheduling & Feedback)
- **Dashboard:** `/api/dashboard/metrics`, `/api/dashboard/application-funnel`
