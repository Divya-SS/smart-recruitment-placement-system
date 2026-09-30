# Smart Recruitment & Placement Management System (SRPMS)

A robust, enterprise-grade full-stack web application designed for end-to-end talent acquisition, candidate screening, rule-based skill matching, interview scheduling, and placement lifecycle tracking.

---

## 🚀 Technology Stack

### Backend
- **Language:** Python 3.10+
- **Framework:** Flask 3.1
- **Database ORM:** Flask-SQLAlchemy & SQLAlchemy 2.0
- **Database Migrations:** Flask-Migrate (Alembic)
- **Authentication:** Flask-JWT-Extended (Stateless JSON Web Tokens with RBAC)
- **Password Security:** Bcrypt
- **Cross-Origin Handling:** Flask-CORS
- **Testing:** Pytest

### Database
- **Database Engine:** MySQL 8.0 (InnoDB)
- **Driver:** PyMySQL

### Frontend (Upcoming Phases)
- **Library:** React 18
- **Build Tool:** Vite
- **Routing:** React Router v6
- **HTTP Client:** Axios (with dynamic auth interceptors)
- **Styling:** TailwindCSS

---

## 📁 Project Structure

```
smart-recruitment-system/
├── backend/
│   ├── app/
│   │   ├── models/             # SQLAlchemy ORM Models (User, Candidate, Job, Application, Interview)
│   │   ├── routes/             # Modular API Blueprints
│   │   ├── services/           # Business Logic Layer & Matching Engine
│   │   ├── schemas/            # Request/Response Validation Schemas
│   │   ├── utils/              # Custom Exceptions, Response Builders, Error Handlers, RBAC
│   │   ├── extensions.py       # Extension bindings (db, jwt, migrate, cors)
│   │   └── __init__.py         # Application Factory (create_app)
│   ├── config/                 # Environment Configuration classes
│   ├── tests/                  # Automated Pytest Test Suite
│   ├── .env.example            # Environment configuration template
│   ├── requirements.txt        # Backend dependencies
│   └── run.py                  # API Server entry point
├── frontend/                   # React Frontend (Upcoming Phases)
├── database/
│   ├── schema.sql              # MySQL DDL table creation script
│   └── seed_data.sql           # Roles and taxonomy seeds
├── docs/                       # Architecture and API documentation
├── .gitignore
└── README.md
```

---

## ⚙️ Backend Local Setup Instructions

### 1. Prerequisites
- **Python 3.10+** installed
- **MySQL 8.0+** running locally or accessible via network

### 2. Set Up Virtual Environment & Dependencies

Navigate to the `backend` folder:
```bash
cd backend
python -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

---

## 🗄️ Database Setup Instructions

### Option A: Initialize Database via MySQL CLI or Workbench
1. Create the database and tables using the provided DDL script:
   ```bash
   mysql -u root -p < ../database/schema.sql
   mysql -u root -p < ../database/seed_data.sql
   ```

### Option B: Initialize Database using Flask-Migrate
1. Ensure your MySQL server is running and create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS recruitment_db;
   ```
2. Run database migrations:
   ```bash
   flask --app run.py db init
   flask --app run.py db migrate -m "Initial schema migration"
   flask --app run.py db upgrade
   ```

---

## 🔑 Environment Variables Configuration

Copy `.env.example` to `.env` inside the `backend/` directory:
```bash
cp .env.example .env
```

Configure your parameters in `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secure_flask_secret_key

PORT=5000
HOST=127.0.0.1

DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=recruitment_db

DATABASE_URL=mysql+pymysql://root:your_mysql_password@localhost:3306/recruitment_db

JWT_SECRET_KEY=your_secure_jwt_secret_key
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRES_DAYS=30

CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## ▶️ Running the Backend Server

Start the Flask development server:
```bash
python run.py
```

Output:
```
=======================================================
🚀 SMART RECRUITMENT & PLACEMENT API SERVER
📡 Running at: http://127.0.0.1:5000/api/health
🔧 Environment: development
=======================================================
```

---

## 🧪 Testing the API

### 1. Test Health Check Endpoint
```bash
curl http://127.0.0.1:5000/api/health
```

Expected Response:
```json
{
  "status": "success",
  "message": "Smart Recruitment API is running"
}
```

### 2. Run Automated Pytest Suite
```bash
pytest
```
